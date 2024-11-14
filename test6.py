class TreeNode:
    def __init__(self,val = 0,left = None,right = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def path_target(self,root:TreeNode,target:int):
        """
        1.寻找二叉树和为目标和的路径
        """


        # def recur(root, tar):
        #     if not root:
        #         return
        #     path.append(root.val)
        #     tar -= root.val
        #     if tar == 0 and not root.left and not root.right:
        #         res.append(list(path))  # res.append(list(path)) ，相当于复制了一个 path 并加入到 res
        #     recur(root.left, tar)
        #     recur(root.right, tar)
        #     re = path.pop()
        #     print(re)
        #
        # res, path = [], []
        # recur(root, target)
        # return res

        def recur(root,target):
            if not root:
                return
            path.append(root.val)
            target -= root.val

            if target == 0 and not root.left and not root.right:
                res.append(path)
            recur(root.left,target)
            recur(root.right,target)
            path.pop()        # 这个才是重点

        res = []
        path = []
        recur(root,target)
        return res




