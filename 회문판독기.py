def judge(s):
    stack = []
    
    # 알파벳만 스택에 넣기
    for ch in s:
        if ch.isalpha():  # 알파벳만 처리
            stack.append(ch.lower())  # 소문자로 변환해서 넣기
    
    # 스택에서 하나씩 꺼내며 비교
    for ch in s:
        if ch.isalpha() and stack.pop() != ch.lower():  # 알파벳일 때만 비교
            return False
    
    return True  # 끝까지 일치하면 회문

# 사용자 입력
a = input("문자열을 입력하세요: ")

if judge(a):
    print("회문입니다 ✅")
else:
    print("회문이 아닙니다 ❌")
