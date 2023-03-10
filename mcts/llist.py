   
class LinkedList:
    def __init__(self):
        self.head = None
        
    def add_first(self, node):
            """Adds a node at the start of the linked list
                Inputs: node - Node() object"""
            node.child = self.head
            self.head = node

    def add_last(self, node):
        """Adds a node at the end of the linked list
            Inputs: node - Node() object"""
        if self.head is None:
            self.head = node
            return
        for current_node in self:
            pass
        node.parent = current_node
        current_node.child = node

    def add_after(self, parent_node_data, new_node):
        """Transerses linked list until it finds a node with data matching
            target_node_data. Adds new_node after that node"""
        if self.head is None:
            raise Exception("list is empty")
        
        for node in self:
            if node.state == parent_node_data:
                new_node.child = node.child
                node.child = new_node
                new_node.parent = node
                return
            
        raise Exception("Node with data '%s' not found" % parent_node_data)
    
    def add_before(self, child_node_data, new_node):
        """Transerses linked list until it finds a node with data matching
            target_node_data. Adds new_node before that node"""
        if self.head is None:
            raise Exception("list is empty")
        if self.head.state == child_node_data:
            self.add_first(new_node)
            return
        
        prev_node = self.head
        for node in self:
            if node.state == child_node_data:
                prev_node.child = new_node
                new_node.child = node
                node.parent = new_node
                return
            prev_node = node

        raise Exception("Node with data '%s' not found" % child_node_data)
    
    def remove_node(self, target_node_data):
        if self.head is None:
            raise Exception("list is empty")
        
        if self.head.state == target_node_data:
            self.head = self.head.child
            return
        
        previous_node = self.head
        for node in self:
            if node.state == target_node_data:
                previous_node.child = node.child
                node.child.parent = previous_node.child
                return
            previous_node = node

        raise Exception("Node with data '%s' not found" % target_node_data)