#authors:
# Vikhyat Gupta
from tkinter import *
import random, time
class Board:
    window = Tk()
    def __init__(self):
        self.board_x = 9
        self.board_y = 9
        self.flag_game_start = True
        self.game_over = False
        self.num_mines = 0
        #list with all the buttons
        self.button_list = [[0] * self.board_y for x in range(self.board_x)]
        #list for all the numbers
        self.gridnumber_list = [[0] * self.board_y for x in range(self.board_x)]
        #list for storing mine positions
        self.mine_positions = []
        #list for storing flag positions
        self.flag_list = []
        self.flag_count = 10
        #list for storing flag status 1:Enabled -1:Diabled 0:cannot be flagged
        self.flag_status_list = [[-1] * self.board_y for x in range(self.board_x)]
        #Images initialised

        self.smiley = PhotoImage(file="temp/new_game_button.png")
        self.button = PhotoImage(file="temp/button.png")
        self.mine = PhotoImage(file="temp/mine.png")
        self.flag = PhotoImage(file="temp/flag.png")
        self.lost = PhotoImage(file="temp/lost.png")
        self.won = PhotoImage(file="temp/won.png")
        self.mine_bad_flag=PhotoImage(file="temp/mine_bad_flag.png")
        self.frame_top = Frame(self.window, width=700, height=1000)
        self.frame_top.pack()
        self.frame_board = Frame(self.window, width=700, height=1000)
        self.frame_board.pack()
        self.flag_remaining = Label(self.frame_top, justify=LEFT, text="Remaining Flags", fg='red')
        self.lbl_flag_count = Label(self.frame_top, justify=LEFT, text=self.flag_count, fg='red')
        self.flag_remaining.pack(side=LEFT, fill=BOTH, expand=True)
        self.lbl_flag_count.pack(side=LEFT, fill=BOTH, expand=True)
        self.btn_status = Button(self.frame_top, image=self.smiley, command=self.start_game)
        self.btn_status.pack(side=LEFT)
        self.lbl_timer = Label(self.frame_top, text='')
        self.lbl_timer.pack(side=RIGHT, fill=BOTH, expand=True)
        self.reset_game()
        self.window.mainloop()

    #reinitialising the board on start click
    def reset_game(self):
        self.lbl_timer.config(text="")
        self.flag_count = 10
        self.lbl_flag_count["text"] = self.flag_count
        self.btn_status.config(image=self.smiley)
        for row in range(self.board_x):
            for col in range(self.board_y):
                self.button_list[row][col] = Button(self.frame_board, width=4, height=2, bg='grey', command=lambda x=row, y=col: self.button_click(x, y))
                self.button_list[row][col].bind("<ButtonPress-3>", lambda event, x=row, y=col: self.place_flag(event, x, y))
                self.button_list[row][col].grid(row=row, column=col)
                self.gridnumber_list[row][col] = 0
                self.flag_status_list[row][col] = -1
                self.mine_positions = []
                self.lbl_timer
        self.flag_list = []
        self.game_over = False
    #starting the game
    def start_game(self):
        self.mine_positions = []
        self.reset_game()
        self.flag_game_start = True


    ###Mines Logic###

    # Generating random postions for mines
    def mine_generate(self):
        mine_pos = [random.randint(0, 8), random.randint(0, 8)]
        return mine_pos

    #checking for duplicate mines
    def check_for_mines(self, row, col):
        new_coord = [row, col]
        is_mine = False
        for x in range(len(self.mine_positions)):
            if self.mine_positions[x] == new_coord:
                is_mine = True
                break
            else:
                is_mine = False
        return is_mine

    #placing mines on random positions
    def place_mines(self):
        new_coordinates = self.mine_generate()
        self.mine_positions.append(new_coordinates)
        num_mines = 1
        while num_mines <= 9:
            new_coordinates = self.mine_generate()
            row = new_coordinates[0]
            col = new_coordinates[1]
            if self.check_for_mines(row, col):
                continue
            else:
                num_mines += 1
                self.mine_positions.append(new_coordinates)
        #calling place numbers in according to mines placed
        self.place_numbers()

    ###  Number Logic ###

    #checking for if number exists at particular position
    def check_for_numbers(self, row, col):
        new_coord = [row, col]
        is_num = False
        if self.gridnumber_list[row][col] > 0:
            is_num = True
        else:
            is_num = False
        return is_num

    # placing numbers around the mine positions
    def place_numbers(self):
        #starting with the (x-1)(y-1) position and traversing through all the positions around each mine
        for x in range(len(self.mine_positions)):
            row = self.mine_positions[x][0] - 1
            col = self.mine_positions[x][1] - 1
            for x in range(0, 3):
                for y in range(0, 3):
                    row_temp = row + x
                    col_temp = col + y
                    new_coordinates = [row_temp, col_temp]
                    if 0 <= row_temp <= 8 and 0 <= col_temp <= 8:
                        if self.check_for_mines(row_temp, col_temp):
                            self.gridnumber_list[row_temp][col_temp] = -1
                            continue
                        else:
                            self.gridnumber_list[row_temp][col_temp] += 1
    #show numbers if clicked on non-mine position
    def show_number(self, row, col):
        self.button_list[row][col].config(relief=SUNKEN, text=self.gridnumber_list[row][col])

    #clearing the grid buttons till the boundary of mines on clicking non-mine position
    def clear(self, row, col):
        row -= 1
        col -= 1
        for r in range(0, 3):
            for c in range(0, 3):
                row_temp = row + r
                col_temp = col + c
                if 0 <= row_temp <= 8 and 0 <= col_temp <= 8:
                    if self.flag_status_list[row_temp][col_temp] == -1:
                        if self.check_for_numbers(row_temp, col_temp):
                                self.show_number(row_temp, col_temp)
                                self.flag_status_list[row_temp][col_temp] = 0
                                # print("Number at pos: ", self.flag_status_list[row_temp][col_temp])
                                continue
                        elif self.check_for_mines(row_temp, col_temp):
                            continue
                        elif self.gridnumber_list[row_temp][col_temp] == 0:
                                self.button_list[row_temp][col_temp].config(relief=SUNKEN)
                                self.flag_status_list[row_temp][col_temp] = 0
                                self.clear(row_temp, col_temp)

        ### Flags Logic ###

    #checking for if flag can be placed or not and increementing the counter
    def place_flag(self, event, row, col):
        new_flag_coordinate = [row, col]
        if self.flag_status_list[row][col] != 0 and self.game_over == False:
            if self.flag_status_list[row][col] == -1:
                if self.flag_count > 0:
                    self.button_list[row][col].config(relief=SUNKEN, width=20, height=15, image=self.flag)
                    self.flag_list.append(new_flag_coordinate)
                    print('Flag list: ',self.flag_list)
                    print("row", row, "col:", col)
                    self.flag_count -= 1
                    self.lbl_flag_count["text"] = self.flag_count
                    self.flag_status_list[row][col] = 1
            else:
                self.remove_flag(row, col)
        if self.flag_count == 0:
            self.win()

    #disabling flags and increementing the counter
    def remove_flag(self, row, col):
        new_flag_coordinate = [row, col]
        self.button_list[row][col].config(relief=RAISED, width=4, height=2, image="")
        self.flag_count += 1
        self.lbl_flag_count["text"] = self.flag_count
        self.flag_status_list[row][col] = -1
        self.flag_list.remove(new_flag_coordinate)
        print(self.flag_list)

    ### Game Logic ####

    #checking for buttons clicked when the game starts
    def button_click(self, row, col):
        #if game starts then place mines randomly
        if self.flag_game_start:
            self.timer()
            self.place_mines()
            self.flag_game_start = False

        if self.flag_status_list[row][col] != 1:
            #checking for mines
            if self.check_for_mines(row, col):
                self.mine_clicked(row, col)
            if self.check_for_numbers(row, col):
                self.show_number(row, col)
            elif self.gridnumber_list[row][col] == 0:
                self.flag_status_list[row][col] = 0
                self.button_list[row][col].config(relief=SUNKEN)
                self.clear(row, col)
      # Game wins if flag positions matches mine positions
    def win(self):
        if not self.mine_positions:
            return 0
        else:
            count=0
            for x in range(len(self.flag_list)):
                for y in range(len(self.flag_list)):
                    if self.flag_list[x] == self.mine_positions[y]:
                        count+=1
            if count==10:
                self.disable_board()
                self.btn_status.config(image = self.won)
                self.game_over = True

    #Game lose if mine is clicked
    def mine_clicked(self, row, col):
        for x in range(len(self.mine_positions)):
            row = self.mine_positions[x][0]
            col = self.mine_positions[x][1]
            self.button_list[row][col]["image"] = self.mine
        for i in range(9):
            for j in range(9):
                if (self.flag_status_list[i][j] == 1 and self.gridnumber_list[i][j] != -1):
                    self.button_list[i][j]["image"] = self.mine_bad_flag
        self.btn_status.config(image=self.lost)
        self.disable_board()


    #disbling the board on game lose or win
    def disable_board(self):
        self.game_over=True
        for x in range(self.board_x):
            for y in range(self.board_y):
                self.button_list[x][y].config(state=DISABLED)
    # reseting the timer
    def timer(self):
        now = int(time.perf_counter())
        self.lbl_timer.configure(text=now)
        self.lbl_timer.after(1000, self.timer)

new_game = Board()