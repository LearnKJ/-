#include <stdio.h>
#include <string.h>

struct List {
    char name[20];
    char phone[13];
    char address[50];
    char date[9];
};

int PrintEveryInfo(struct List *li, int cnt);
int AddInfo(struct List *li, int *cnt);
int SearchInfo(struct List *li, int *cnt);
int DeleteInfo(struct List *li, int *cnt);

int main(){
    struct List list[100];
    int input = 0, cnt = 0;
    
    while (input != 5){
        printf("------주소록 프로그램------\n");
        printf("-원하시는 기능의 숫자를 입력하세요-\n");
        printf("(1) 목록보기\n");
        printf("(2) 추가하기\n");
        printf("(3) 탐색하기\n");
        printf("(4) 삭제하기\n");
        printf("(5) 종료하기\n");
        printf("숫자를 입력하세요: ");
        scanf("%d", &input);

        if (input == 1) {
            PrintEveryInfo(list, cnt);
        } else if (input == 2) {
            AddInfo(list, &cnt);
        } else if (input == 3) {
            SearchInfo(list, &cnt);
        } else if (input == 4) {
            DeleteInfo(list, &cnt);
        } else if (input == 5) {
            printf("프로그램을 종료합니다.\n");
        } else {
            printf("올바른 숫자를 입력하세요.\n");
        }
    }
    
    return 0;
}

int AddInfo(struct List *li, int *cnt){
    printf("이름을 입력해주세요: ");
    scanf("%s", li[*cnt].name);
    printf("전화번호를 입력해주세요: ");
    scanf("%s", li[*cnt].phone);
    printf("주소를 입력해주세요: ");
    scanf("%s", li[*cnt].address);
    printf("생일을 입력해주세요: ");
    scanf("%s", li[*cnt].date);
    
    *cnt += 1;
    
    printf("\n---- 입력 종료 ----\n");
    
    return 0; 
}

int PrintEveryInfo(struct List *li, int cnt){
    if (cnt < 1){
        printf("등록된 정보가 없습니다. 정보를 먼저 등록해주세요.\n");
        return 0;
    }

    printf("등록된 정보 %d개 \n", cnt);
    for (int i = 0; i < cnt; i++){
        printf("(이름: %s / 전화번호: %s / 주소: %s / 생년월일: %s)\n", 
                li[i].name, li[i].phone, li[i].address, li[i].date);
    }
    
    printf("\n---- 출력 종료 ---- \n");
    
    return 0;
}

int SearchInfo(struct List *li, int *cnt){
    char search_str[20];
    int check = 0;

    if (*cnt < 1){
        printf("등록된 정보가 없습니다. 정보를 먼저 등록해주세요.\n");
        return 0;
    }

    printf("이름으로 정보 검색: ");
    scanf("%s", search_str);
    
    for (int i = 0; i < *cnt; i++){
        if (strcmp(li[i].name, search_str) == 0){
            printf("(이름: %s / 전화번호: %s / 주소: %s / 생년월일: %s)\n", 
                    li[i].name, li[i].phone, li[i].address, li[i].date);
            check += 1;
        }
    } 
    
    if (check == 0){
        printf("검색 결과를 찾을 수 없습니다.\n");
    }

    printf("\n---- 검색 종료 ---- \n");
    
    return 0;
}

int DeleteInfo(struct List *li, int *cnt){
    int index;
    
    if (*cnt < 1){
        printf("등록된 정보가 없습니다. 정보를 먼저 등록해주세요.\n");
        return 0;
    }
    
    for (int i = 0; i < (*cnt); i++){
        printf("(%d) (이름: %s / 전화번호: %s / 주소: %s / 생년월일: %s)\n", 
                i + 1, li[i].name, li[i].phone, li[i].address, li[i].date);
    }

    printf("삭제할 항목의 번호 입력: ");
    scanf("%d", &index);
    
    if (index < 1 || index > *cnt) {
        printf("잘못된 입력입니다.\n");
        return 0;
    }

    for (int i = index - 1; i < (*cnt) - 1; i++){
        li[i] = li[i + 1];
    } 
    
    *cnt -= 1;
    
    printf("\n---- 삭제 완료 ----\n");
    
    return 0; 
}
