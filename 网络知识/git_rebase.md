```bash
Git 
Delete remote branch
git push origin --delete carcare1_csv_import
Delete local branch
git branch -d carcare1_csv_import
Remove commit and history
Git rebase -i commitid

Then you will go to vi:
pick 2231360 some old commit
pick ee2adc2 Adds new feature





# Rebase 2cf755d..ee2adc2 onto 2cf755d (9 commands)
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# x, exec = run command (the rest of the line) using shell
# d, drop = remove commit

Change pick to drop then it will remove the commit

```