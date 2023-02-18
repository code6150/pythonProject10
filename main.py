import sys
# 각 개인이 정보를 저장할 클래스 생성 ( Person )
# 저장할 데이터 (이름, 전화번호, 주소)
#   - 생성자를 통해 해당 정보들을 전달 받습니다.
#   - info() 메소드를 구현합니다. ( 저장된 정보를 출력하는 메소드 )
#       -이름, 전화번호, 주소

class Method:
    def __init__(self, func, desc):
        self.func = func
        self.desc = desc

class Person:

    # 함수 () <- 괄호 안에서 만들어지는 변수 = 매개변수
    # 매개 변수, 지역 변수
    #   - 해당 함수가 종료되면 함께 소멸함.

    # 데이터가 온전히 클래스와 함께 저장되려면, = 멤버(인스턴스) 변수
    # 인스턴스 변수
    #   - self.이름
    def __init__(self, name, phone, address):
        self.name = name
        self.phone = phone
        self.address = address

    def info(self):
        print(self.name, self.address, self.phone, sep=',')

# 이번 프로젝트의 모든 기능들  AddressBook 이라는 클래스가 포함하고 있다.
# Person 객체를 여러개 저장할 수 있습니다. ( address_list: list )
# AddressBook 클래스가 구현 할 메소드 목록은 아래와 같습니다.

class AddressBook:

    def __init__(self):
        self.address_list = []
        self.file_reader()
        self.method_list = (
            Method(self.exit, "프로그램 종료"),
            Method(self.insert, "신규 주소록 추가"),
            Method(self.delete, "기존 주소록 삭제"),
            Method(self.update, "기존 주소록 수정"),
            Method(self.search, "기존 주소록 검색"),
            Method(self.print_all, "전체 주소록 출력")
        )

    def file_reader(self):
        # address_list 에 추가 Person 객체로 바꿔서...
        try:
            with open('addressBook.csv', 'r', encoding='utf-8') as f:
                for data in f.readlines():
                    data.rstrip('\n')
                    data_list = data.split(',')
                person = Person(data_list[0], data_list[1], data_list[2])
                self.address_list.append(person)
        except FileNotFoundError:
            print('파일 없는데?')

    def file_generator(self):
        with open('addressBook.csv', 'w', encoding='utf-8') as f:
            for person in self.address_list:
                f.write(f'{person.name},{person.phone},{person.address}\n')

    def menu(self):
        # 사용자에게 메뉴를 출력하고 선택한 값을 입력받아 해당 값을 리턴 합니다. ( int )
        print('='*30)
        for index, menu in enumerate(self.method_list):
            if index == 0: continue
            print(f'{index}. {menu.desc}')
        print(f'0. {self.method_list[0].desc}')
        print('=' * 30)
        return int(input('수행할 작업을 숫자로 입력하세요 >>> '))

    def exit(self):
        """프로그램 종료"""
        print('프로그램을 종료합니다.')
        sys.exit()

    def run(self):
        while(True):
            choice = self.menu()
            if 0 > choice >= len(self.method_list):
                print("없는 명령입니다.")
                continue
            self.method_list[choice].func()

    def insert(self):
        """신규 주소록 등록"""
        # 사용자로 부터 새로 등록할 이름, 번호, 주소를 입력받은 뒤 이를 이용해서 Person 객체를 생성하고,
        # 이 Person 객체를 address_list 에 추가 합니다.
        # 그리고 곧 바로 file_generator() 메소드를 호출해서 변경된 address_list 를 저장합니다.
        print('=== 신규 주소록 추가 ===')
        name = input('이름 입력 : ')
        phone = input('번호 입력 : ')
        address = input('주소 입력 : ')
        # True -> False 이외의 모든 값
        # False -> 비어있거나, None이거나, 0, [], '', ...
        if not name or not phone or not address:
            print('제대로 입력하세요')
            return
        person = Person(name, phone, address)
        self.address_list.append(person)
        self.file_generator()
        pass

    def delete(self):
        """기존 주소록 삭제"""
        # 이름을 입력받아서 해당 이름의 Person 을 삭제 (address_list)
        # 동일한 이름이 2개 이상 저장되어있는 경우를 대비하여 삭제 전에 확인 과정을 거칩니다.
        # 삭제하려는 전화번호가 맞는지? (Y/N) 기본값 y
        #   -n -> 동일한 이름의 다른 Person 이 있으면 그것에 대해서도 물어봄.
        #   - 동일한 이름이 더 이상 없을 경우, {} 의 정보가 삭제되지 않았습니다.
        #   - 삭제한 경우, {] 의 정보가 삭제되엇습니다.
        # 삭제를 성공하면 file_generator 를 호출하여 파일 새로 저장
        print('=== 기존 주소록 삭제 ===')
        name = input('이름을 입력하세요 : ')
        if not name:
            print('이름을 입력하지 않았습니다.')
            return

        for person in self.address_list:
            if person.name == name:
                select = input(f'삭제하려는 {name}의 번호가 {person.phone} 입니까? (Y/N)')
                if not select or select == 'Y' or select == 'y':
                    self.address_list.remove(person)
                    print(f'{name}님의 정보를 삭제 했습니다.')
                    return
                elif select == 'n' or select == 'N':
                    continue
                else:
                    print('잘못된 입력입니다.')
                    return

        #return 을 만나지 못 한 경우.
        print(f'일치하는 {name} 님의 정보가 존재하지 않습니다.')

    def update(self):
        """기존 주소록 수정"""
        print('=== 기존 주소록 수정 ===')
        name = input('수정할 이름 입력 : ')
        if not name:
            print('이름을 입력하지 않았습니다.')
            return

        for person in self.address_list:
            modify = False
            if person.name == name:
                select = input(f'수정하려는 {name} 님의 번호가 {person.phone} 이 맞나요? (Y/N) ')
                if not select or select == 'y' or select == 'Y':
                    phone = input('수정할 번호 입력 : ')
                    if phone:
                        person.phone = phone
                        print('번호가 수정되었습니다.')
                        modify = True
                    address = input('수정할 주소를 입력 : ')
                    if address:
                        person.address = address
                        print('주소가 수정되었습니다.')
                        modify = True
                    if modify:
                        self.file_generator()
                        return
        # ?? for문이 끝날 때 까지 return을 만나지 못 했다 -> modify 가 True 가 된적이 없다 -> 수정이 한 번도 이루어지지 않았다.
        print(f'{name} 의 정보가 수정되지 않았습니다.')


    def print_all(self):
        """기존 주소록 출력"""
        pass

    def search(self):
        print('아직 구현중인 기능입니다.')
        """기존 주소록 검색"""
        pass

AddressBook().run()