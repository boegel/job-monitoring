"""
Module with data on the cluster - mainly on Hopper, but extensible

Classes and functions
=====================

"""
#===============================================================================    
def hopper_mem_avail_gb(node):
    """
    Return the memory available on a compute node on Hopper.
    
    :param str node: name of a compute node.
    :return: number of GB of memory available to the user on that node. 
    
    If *node* is a list of node names the total memory available is summed over 
    the nodes in the list. 
    """
    if isinstance(node,str):
        r = node[1]
        if r!='5':
            return 58
        c = node[3]
        if not c in '123':
            return 58
        cn = node[7]
        if not cn in '12345678':
            return 58
        return 256 # r5c[1-3]cn0[1-8]
    elif isinstance(node,list):
        mem = 0
        for ni in node:
            mem += hopper_mem_avail_gb(ni)
        return mem
    else:
        raise TypeError('Expected str, or list of str, got '+str(type(node)))
#===============================================================================
def hopper_ncores_per_node(node):
    """
    Return the number of cores of a compute node on Hopper.
    
    :param str node: name of a compute node.
    :return: number of cores on that node. 
    """
    return 20
#===============================================================================    
cluster_properties = {'hopper':{'ncores_per_node' : hopper_ncores_per_node
                               ,'login_nodes'     :['login.hpc.uantwerpen.be'
                                                   ,'login1-hopper.uantwerpen.be'
                                                   ,'login2-hopper.uantwerpen.be'
                                                   ,'login3-hopper.uantwerpen.be'
                                                   ,'login4-hopper.uantwerpen.be']
                               ,'mem_avail_gb'    : hopper_mem_avail_gb
                               }
                     }
#===============================================================================    
current_cluster = 'hopper'
""" name of the cluster which we are monitoring."""
#===============================================================================    

#===============================================================================    
#== test code below ============================================================
#===============================================================================    
if __name__=="__main__":
    
    node_fmt = 'r5c{}cn0{}'
    for c in range(1,4):
        for cn in range(1,9):
            node = node_fmt.format(c,cn)
            assert hopper_mem_avail_gb(node)==256
            
    node_fmt = 'r6c{}cn0{}'
    for c in range(1,4):
        for cn in range(1,9):
            node = node_fmt.format(c,cn)
            assert hopper_mem_avail_gb(node)==58

    print('\n--finished--')
