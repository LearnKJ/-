import json
import difflib
import os

class SmartDictionary:
    def __init__(self, filename="words.json"):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            return {"apple": "사과", "banana": "바나나", "code": "코드, 암호", "python": "파이썬 프로그래밍 언어"}
        
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print("💾 데이터가 저장되었습니다.")

    def search(self, word):
        word = word.lower()

        if word in self.data:
            return f"📖 {word}: {self.data[word]}"
        
        matches = difflib.get_close_matches(word, self.data.keys(), n=1, cutoff=0.6)
        
        if matches:
            similar_word = matches[0]
            choice = input(f"🤔 '{word}'을(를) 찾으셨나요? 혹시 '{similar_word}'인가요? (Y/N): ").lower()
            if choice == 'y':
                return f"📖 {similar_word}: {self.data[similar_word]}"
            else:
                return "❌ 단어를 찾을 수 없습니다."
        else:
            return "❌ 단어를 찾을 수 없으며, 유사한 단어도 없습니다."

    def add_word(self):
        word = input("추가할 영단어: ").lower()
        if word in self.data:
            print(f"이미 존재하는 단어입니다! ({word}: {self.data[word]})")
            return

        meaning = input(f"'{word}'의 뜻: ")
        self.data[word] = meaning
        self.save_data()
        print(f"✅ '{word}' 단어가 추가되었습니다.")

    def delete_word(self):
        word = input("삭제할 단어: ").lower()
        if word in self.data:
            del self.data[word]
            self.save_data()
            print(f"🗑️ '{word}' 단어가 삭제되었습니다.")
        else:
            print("❌ 삭제할 단어가 목록에 없습니다.")

def main():
    my_dict = SmartDictionary()
    
    print("=== 📚 나만의 스마트 단어장 (JSON 기반) ===")
    
    while True:
        print("\n[1]검색  [2]추가  [3]삭제  [4]전체목록  [5]종료")
        choice = input("선택: ")

        if choice == '1':
            q = input("검색할 단어 (예: appl): ")
            print(my_dict.search(q))
        elif choice == '2':
            my_dict.add_word()
        elif choice == '3':
            my_dict.delete_word()
        elif choice == '4':
            print(f"\n📑 현재 저장된 단어 ({len(my_dict.data)}개):")
            for k, v in my_dict.data.items():
                print(f"- {k}: {v}")
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()
