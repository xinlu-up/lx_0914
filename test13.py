# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        def dfs(root):
            if not root:
                return 0
            left_part = dfs(root.left)
            right_part = dfs(root.right)
            self.ans = max(self.ans, left_part + root.val + right_part)  # 9
            return max(0, root.val, root.val + left_part, root.val + right_part)  # 证明哪一路是最大的。  这个地方就是选取最大的一路作为和其他的合并。

        self.ans = root.val  # -10
        dfs(root)
        return self.ans

def create_tree(val_list):
    """
    1.构建二叉树
    """
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    return root

if __name__ == "__main__":
    val_list= [-10,9,20,15,7]
    root = create_tree(val_list)

    sol = Solution()
    res = sol.maxPathSum(root)
    print(res)





