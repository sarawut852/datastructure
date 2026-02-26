stack = []

pair = {')':'(', '}':'{', ']':'['}
opens = set(pair.values())
expr = input("Enter  expression wite brackets :")
valid = True
for ch in expr:
    if ch in opens:
        stack.append(ch)
        print("push :" ,ch, "stack now :", stack)

    elif ch in pair:
        if not stack:
            print("Error : stack empty bu found closing bracket :", ch)
            valid = False
            break

        top = stack.pop()
        print("pop :", top, "for clossing ", ch, "stack = :", stack)

        if top != pair[ch]:
            print("Error : bracket not match -> ", top, " vs ", ch)
            valid = False
            break

if valid:
    if stack:
        print("Error : still ", stack)
        valid = False

if valid:
    print("result : Valid")
else:
    print("result : Invalid")


#print("Result of operate : " , xxxx)