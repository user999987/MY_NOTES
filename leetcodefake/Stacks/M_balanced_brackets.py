def balancedBrackets(string):
    # Write your code here.
    stack = []
    for i in range(0, len(string)):
        char = string[i]
        if not isBracket(char):
            continue
        if len(stack) == 0 or not pushOrPop(stack[-1], char):
            stack.append(char)
        else:
            stack.pop()

    print(stack)
    return True if len(stack) == 0 else False


def isBracket(char):
    if char != "(" and char != ")" and char != "[" and char != "]" and char != "{" and char != "}":
        return False
    else:
        return True


def pushOrPop(stackVal, curVal):
    if (stackVal == "("
            and curVal == ")") or (stackVal == "{"
                                   and curVal == "}") or (stackVal == "["
                                                          and curVal == "]"):

        return True
    else:
        return False
