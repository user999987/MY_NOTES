# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:
    
    def serialize(self, root):
        se_res=[]
        def process(root):
            if root is None:
                se_res.append("None")
                return 
            se_res.append(str(root.val))
            process(root.left)
            process(root.right)
        process(root)
       
        return " ".join(se_res)
        

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        dl = data.split(' ')
       
        def buildTree(dl):
            if dl:
                val = dl.pop(0)
                if val == 'None':
                    return None
                root=TreeNode(int(val))
                root.left=buildTree(dl)
                root.right=buildTree(dl)
                return root
        return buildTree(dl)

        

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))