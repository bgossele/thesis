'''
Created on Mar 16, 2015

@author: brecht
'''
import abc
from multiprocessing import Pipe
from multiprocessing.process import Process
from cassandra.cluster import Cluster
import array
import sys
from multiprocessing.synchronize import Event

class Expression(object):
    
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evaluate(self, session, starting_set):
        return

    @abc.abstractmethod
    def can_prune(self):
        return True

class Basic_expression(Expression):
    
    def __init__(self, from_table, select_column, where_clause):
        self.table = from_table
        self.select_column = select_column
        self.where_clause = where_clause
  
    def evaluate(self, socket, starting_set):
        
        if len(starting_set) == 0:
            return set()
        
        query = "SELECT %s FROM %s" % \
            (self.select_column, self.table)
        if self.where_clause != "":
            query += " WHERE %s" % self.where_clause            
        '''if self.can_prune() and not starting_set == "*":
            if self.table.startswith('samples'):
                in_clause = "','".join(starting_set)            
                query += " AND %s IN ('%s')" % \
                    (self.select_column, in_clause)
            else:
                in_clause = ",".join(map(str, starting_set))            
                query += " AND %s IN (%s)" % \
                    (self.select_column, in_clause)   '''  
        return async_rows_as_set(socket, query)
    
    def can_prune(self):
        return not any (op in self.where_clause \
                        for op in ["<", ">"])

    def __str__(self):
        return self.where_clause
    
class AND_expression(Expression):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, session, starting_set):
        
        if len(starting_set) == 0:
            return set()
        
        '''if self.right.can_prune():
            temp = self.left.evaluate(session, starting_set)
            return self.right.evaluate(session, temp)
        elif self.left.can_prune():
            temp = self.right.evaluate(session, starting_set)
            return self.left.evaluate(session, temp)
        else:
            temp = self.left.evaluate(session, starting_set)
            return temp & self.right.evaluate(session, temp)'''
         
        temp = self.left.evaluate(session, starting_set)
        return temp & self.right.evaluate(session, temp)        

    def __str__(self):
        res = "(" + str(self.left) + ")" + " AND " + "(" + str(self.right) + ")"
        return res

    def can_prune(self):
        return True
    
class OR_expression(Expression):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
 
    def evaluate(self, session, starting_set):
        
        if len(starting_set) == 0:
            return set()        
        return (self.left.evaluate(session, starting_set) | self.right.evaluate(session, starting_set))

    def __str__(self):
        res = "(" + str(self.left) + ")" + " OR " + "(" + str(self.right) + ")"
        return res

    def can_prune(self):
        return True
    
class NOT_expression(Expression):
    
    def __init__(self, exp, table, select_column, total_nr_variants):
        self.body = exp
        self.table = table
        self.select_column = select_column
        self.total_nr_variants = total_nr_variants
 
    def evaluate(self, session, starting_set):
        
        if len(starting_set) == 0:
            return set()        
        elif starting_set == '*':
            if self.table == 'variants':
                correct_starting_set = set(range(1, self.total_nr_variants+1))
            else:
                correct_starting_set = async_rows_as_set(session, "SELECT %s FROM %s" % (self.select_column, self.table))            
        else:
            correct_starting_set = starting_set
        
        '''if self.table == 'variants' and starting_set == "*":
            return correct_starting_set - self.body.evaluate(session, "*")
        else:
            return correct_starting_set - \
                self.body.evaluate(session, correct_starting_set)'''
        return correct_starting_set - \
                self.body.evaluate(session, correct_starting_set)
                
    def __str__(self):
        return "NOT (" + str(self.body) + ")"

    def can_prune(self):
        return True
    
class GT_wildcard_expression(Expression):
    
    def __init__(self, column, wildcard_rule, rule_enforcement, sample_names, db_contact_points, keyspace, n_variants, cores_for_eval = 1):
        self.column = column
        self.wildcard_rule = wildcard_rule
        if rule_enforcement.startswith('count'):
            self.rule_enforcement = 'count'
            self.count_comp = rule_enforcement[5:].strip()
        else:
            self.rule_enforcement = rule_enforcement        
        self.names = sample_names
        self.nr_cores = cores_for_eval
        self.db_contact_points = db_contact_points
        self.keyspace = keyspace
        self.n_variants = n_variants
        
    def __str__(self):
        return "[%s].[%s].[%s].[%s]" % (self.column, ','.join(self.names), self.wildcard_rule, self.rule_enforcement)
    
    def can_prune(self):
        return True
    
    def evaluate(self, session, starting_set):
        
        step = len(self.names) / self.nr_cores
    
        procs = []
        conns = []
        results = []
        
        invert = False
        invert_count = False
        if self.wildcard_rule.startswith('!'):
            corrected_rule = self.wildcard_rule[1:]
            if self.rule_enforcement == 'all':
                target_rule = 'any'
                invert = True
            elif self.rule_enforcement == 'any':
                target_rule = 'all'
                invert = True
            elif self.rule_enforcement == 'none':
                target_rule = 'all'
            elif self.rule_enforcement.startswith('count'):
                target_rule = 'count'
                invert_count = True
        else:
            target_rule = self.rule_enforcement
            corrected_rule = self.wildcard_rule
            
        if starting_set == "*":
            correct_starting_set = range(1,self.n_variants+1)
        else:
            correct_starting_set = starting_set
        
        for i in range(self.nr_cores):
            parent_conn, child_conn = Pipe()
            conns.append(parent_conn)
            p = Process(target=eval(target_rule +'_query'),\
                args=(child_conn, self.column, corrected_rule, self.db_contact_points, self.keyspace))
            procs.append(p)
            p.start()
        
        #Split names in chunks and communicate to procs
        for i in range(self.nr_cores):
            n = len(self.names)
            begin = i*step + min(i, n % self.nr_cores)
            end = begin + step
            if i < n % self.nr_cores:
                end += 1  
            conns[i].send(self.names[begin:end]) 
            conns[i].send(correct_starting_set)               
        
        #Collect results
        for i in range(self.nr_cores):
            results.append(conns[i].recv())
            conns[i].close()
        
        for i in range(self.nr_cores):
            procs[i].join()
        
        res = set()    
        
        if target_rule == 'any':
            for r in results:
                res = res | r
        elif target_rule in ['all', 'none']:
            res = results[0]
            for r in results[1:]:
                res = res & r
                                
        if invert:
            res = set(correct_starting_set) - res
        
        if target_rule == 'count':
            res_dict = {x: 0 for x in correct_starting_set}
            for sub_result_dict in results:
                for var, count in sub_result_dict.iteritems():
                    res_dict[var] += count     
            if invert_count:
                total = len(self.names)
                for variant, count in res_dict.iteritems():
                    res_dict[variant] = total - count
            res = set([variant for variant, count in res_dict.iteritems() \
                       if eval(str(count) + self.count_comp)])
        
        return res
 
def all_query(conn, field, clause, contact_points, keyspace):
        
    cluster = Cluster(contact_points)
    session = cluster.connect(keyspace)
    
    names = conn.recv()
    initial_set = conn.recv()
  
    results = set(initial_set)
    
    for name in names:
        
        if len(results) == 0:
            break
        
        query = "SELECT variant_id FROM variants_by_samples_%s WHERE sample_name = '%s' AND %s %s " % (field, name, field, clause)
       
        results = async_rows_as_set(session, query) & results
        
    session.shutdown()   
    
    conn.send(results)
    conn.close()

def any_query(conn, field, clause, contact_points, keyspace):
        
    cluster = Cluster(contact_points)
    session = cluster.connect(keyspace)
    
    names = conn.recv()
    initial_set = set(conn.recv())
    
    results = set()
    
    for name in names:
        
        query = "SELECT variant_id FROM variants_by_samples_%s WHERE sample_name = '%s' AND %s %s " % (field, name, field, clause)
        
        row = async_rows_as_set(session, query)
        results = row | results
        
    session.shutdown()  
    
    results = initial_set & results 
    
    conn.send(results)
    conn.close()

def none_query(conn, field, clause, contact_points, keyspace):
        
    cluster = Cluster(contact_points)
    session = cluster.connect(keyspace)
    
    names = conn.recv()
    initial_set = conn.recv()
    
    results = set(initial_set)
    
    for name in names:
        
        query = "SELECT variant_id FROM variants_by_samples_%s WHERE sample_name = '%s' AND %s %s " % (field, name, field, clause)
        
        variants = async_rows_as_set(session, query)
        results = results - variants
        
    session.shutdown()   
    
    conn.send(results)
    conn.close()   
    
def count_query(conn, field, clause, contact_points, keyspace):
    
    cluster = Cluster(contact_points)
    session = cluster.connect(keyspace)    
    names = conn.recv()   
    initial_set = set(conn.recv()) 
    results = dict()
    
    for name in names:        
        query = '''SELECT variant_id FROM variants_by_samples_%s \
                WHERE sample_name = '%s' AND %s %s ''' % (field, name, field, clause)   
        
        variants = initial_set & async_rows_as_set(session, query)
        results = add_row_to_count_dict(results, variants)
        
    session.shutdown()       
    conn.send(results)
    conn.close()
    
def add_row_to_count_dict(res_dict, variants):
    
    for var in variants:
        if not var in res_dict:
            res_dict[var] = 1
        else:
            res_dict[var] += 1    
    return res_dict   

def async_rows_as_set(session, query):
    
    future = session.execute_async(query)
    handler = PagedResultHandler(future)
    handler.finished_event.wait()
    
    if handler.error:
        sys.stderr.write("Query failed: %s\n" % query)
        raise handler.error
    else:    
        return handler.res

class PagedResultHandler(object):

    def __init__(self, future):
        self.error = None
        self.finished_event = Event()
        self.future = future
        self.future.add_callbacks(
            callback=self.handle_page,
            errback=self.handle_error)
        self.res = set()

    def handle_page(self, results):
        
        for row in results:            
            self.res.add(row[0])

        if self.future.has_more_pages:
            self.future.start_fetching_next_page()
        else:
            self.finished_event.set()

    def handle_error(self, exc):
        self.error = exc
        self.finished_event.set()
