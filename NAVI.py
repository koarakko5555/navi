import math
import pygame
#from pygame.locals import *
import sys
import random
import itertools

SCR_RECT = Rect(0, 0, 960, 960) # 画面サイズ
Map_select,Point_select,Play_pre,Play = (0,1,2,3)
dx = (0,-1,-1,-1,0,1,1,1) #global
dy = (1,1,0,-1,-1,-1,0,1)
d_m = ("→","↗","↑","↖","←","↙","↓","↘");
d_c = (1,math.sqrt(2),1,math.sqrt(2),1,math.sqrt(2),1,math.sqrt(2))
d_size = 100 #map_size こいつとcostは初期化が１回しかされないため2回以上探索するなら用検討
cost = [[10000 for i in range(d_size)] for j in range(d_size)] #map_cost すべての座標初期値=10000
st = []
cnt = 0
#colorlist = [(0,0,0),(100,0,0),(0,100,0),(0,0,100),(100,100,0),(100,0,100),(0,100,100),(100,100,100)] #色を表示
cnt = 0 #ループの回数保存 線の色を変えるときに使
final_route_x = [] #最終的なルートのx座標をすべて記録
final_route_y = [] #最終的なルートのｙ座標をすべて記録
final_r = []




class Map1:
    # マップデータ
    map =  [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 7, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0,10, 0, 0, 1],
        [1, 0, 5, 1, 1, 3, 0,10, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0,10, 0, 2, 0, 2, 0, 0, 1],
        [1, 0, 0, 5, 7, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 2, 0, 1, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    row,col = len(map), len(map[0]) # マップの行数,列数を取得
    imgs = [None] * 256             # マップチップ
    msize = 96                   # 1マスの大きさ[px]
    # マップの描画
    def draw(self, screen):
        for i in range(self.row):
            for j in range(self.col):
                screen.blit(self.imgs[self.map[i][j]], (j*self.msize,i*self.msize))




# マップのクラス
class Map2:
    map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 5, 3, 0, 1],
        [1, 0, 5, 1, 6, 0, 0, 2, 0, 0, 0, 0, 1, 0, 9, 3, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 9, 1, 1, 3, 0, 0, 1, 1, 7, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 5, 1, 0, 1, 0, 0, 5, 3, 0, 1, 0,10, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,10, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 5, 3, 0, 0, 1, 0, 0, 0, 0, 0, 4, 0, 5, 3, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 1, 3, 0, 0, 0, 0, 1, 0,10, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 3, 0, 5, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    row,col = len(map), len(map[0]) # マップの行数,列数を取得
    imgs = [None] * 256             # マップチップ
    msize = 48                      # 1マスの大きさ[px]
    # マップの描画
    def draw(self, screen):
        for i in range(self.row):
            for j in range(self.col):
                screen.blit(self.imgs[self.map[i][j]], (j*self.msize,i*self.msize))




class Map3:
    # マップデータ
    map = [[1 for i in range(40)] for j in range(40)]
    for i in range(1,40-1):
        for j in range(1,40-1):
            k = random.random()
            if k<=0.5:
                map[j][i] = 0
            else:
                continue
    row,col = len(map), len(map[0]) # マップの行数,列数を取得
    imgs = [None] * 256             # マップチップ
    msize = 24                    # 1マスの大きさ[px]
    # マップの描画
    def draw(self, screen):
        for i in range(self.row):
            for j in range(self.col):
                screen.blit(self.imgs[self.map[i][j]], (j*self.msize,i*self.msize))




# 画像の読み込み
def load_img(filename, colorkey=None):
    img = pygame.image.load(filename)
    img = img.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0,0))
        img.set_colorkey(colorkey, RLEACCEL)
    return img




def han(point_x,point_y,n_cost,data,cost): #8方向ダイクストラ法 ほぼ全探索しているので計算時間は大きい
    for i in range(8): #すべての方角をためすため 0～7までまわす
        x = point_x+dx[i] #その方向へ進んだときに到達した行
        y = point_y+dy[i] #その方向へ進んだときに到達した列
        if data[x][y] == 0 and cost[x][y]>(n_cost+d_c[i]): #前回までのコストとその方角に進んだ時にかかるコストの合計が今までで一番小さかったら更新、更新出来なかったらその経路は再帰文に入らないので消去したのとほぼ同義
            cost[x][y] = n_cost + d_c[i]
            han(x,y,cost[x][y],data,cost)




def path_a(st,point_x,point_y,st_row,st_col,cost): #道順を逆からたどる
    for i in range(8): #すべての方角をためすため 0～7までまわす
        x = point_x+dx[i] #その方向へ進んだときに到達した行
        y = point_y+dy[i] #その方向へ進んだときに到達した列
        if abs(cost[x][y]-(cost[point_x][point_y] - d_c[i])) <= 0.0000000001: #進んだ先のコスト=(今いる場所のコスト-進んだ先の方向へ進む場合の移動コスト)
            if x==st_row and y==st_col:
                st.append([x,y,d_m[i]])
                break
            else:
                st.append([x,y,d_m[i]])
                path_a(st,x,y,st_row,st_col,cost)
                break




def solve(s1,s2,data,d_size,p_x_route,p_y_route):
    global cnt
    st_row = int(s1[1]) #始点のy座標取得 配列的には列
    st_col = int(s1[0]) #始点のy座標取得 配列的には行
    fi_row = int(s2[1])
    fi_col = int(s2[0])
    print(st_row,st_col,fi_row,fi_col)
    cost = [[10000 for i in range(d_size)] for j in range(d_size)]
    if data[st_row][st_col] == 1: #障害物をクリックしたときの処理
        print("そこは障害物ですst",st_col,st_row)
        return 0
    if data[fi_row][fi_col] == 1:
        print("そこは障害物ですfi",fi_col,fi_row)
        return 0
    for i in range(8):
        cost[st_row][st_col] = 0
        n_cost = 0
        x = st_row+dx[i]
        y = st_col+dy[i]
        if data[x][y] == 0 and cost[x][y] > (n_cost + d_c[i]):
            n_cost += d_c[i]
            cost[x][y] = n_cost    
            han(x,y,n_cost,data,cost)
    print("-------------------------------------------")
    st = []
    path_a(st,fi_row,fi_col,st_row,st_col,cost)
    row_a = []
    col_a = []
    row_a.append(fi_col)
    col_a.append(fi_row)

    for i in range(len(st)):
        row_a.append(st[i][1])
        col_a.append(st[i][0])
    print("cost:",cost[fi_row][fi_col])
    cnt += 1
    p_x_route.append(row_a)
    p_y_route.append(col_a)
    return cost[fi_row][fi_col]




def change_sale(tmp_route_x,tmp_route_y): #routeの中身前後入れ替え
    tmp_len_n = len(tmp_route_x)
    half_route_len = int(tmp_len_n/2)
    for i in range(half_route_len):
        tmp_x = tmp_route_x[i]
        tmp_route_x[i] = tmp_route_x[tmp_len_n-1]
        tmp_route_x[tmp_len_n-1] = tmp_x
        tmp_y = tmp_route_y[i]
        tmp_route_y[i] = tmp_route_y[tmp_len_n-1]
        tmp_route_y[tmp_len_n-1] = tmp_y
        tmp_len_n -= 1
    final_route_x.append(tmp_route_x)
    final_route_y.append(tmp_route_y)




def sale(p_and_cost,p_x_route,p_y_route,point_n): #セールスマン巡回
    point_tmp = [i for i in range(point_n)]
    cob_list = list(itertools.permutations(point_tmp))
    min = 0
    for i in range(point_n-1):
        min+=p_and_cost[i][i+1]
    min += p_and_cost[point_n-1][0]
    min_id = 0
    cnt = 0 #globalで定義してsolve()内でも使ってるのでプログラムを拡張するとき注意
    while cob_list[cnt][0]==0: #(point_n-1)!通り
        sum = 0
        for i in range(point_n-1):
            sum += p_and_cost[cob_list[cnt][i]][cob_list[cnt][i+1]]
        sum += p_and_cost[cob_list[cnt][point_n-1]][0]
        if min>sum:
            min = sum
            min_id = cnt
        cnt+=1
    print(min,min_id)
    print(cob_list[min_id])
    for i in range(point_n-1):
        id_n = point_n-1
        tmp_n = 0
        flag = 0
        a = sorted([cob_list[min_id][i],cob_list[min_id][i+1]])
        if a[0] == cob_list[min_id][i]:
            flag = 1
        for j in range(a[0]):
            tmp_n += id_n
            id_n -= 1
        if flag == 1:
            change_sale(p_x_route[tmp_n+a[1]-a[0]-1],p_y_route[tmp_n+a[1]-a[0]-1])
        else:
            final_route_x.append(p_x_route[tmp_n+a[1]-a[0]-1])
            final_route_y.append(p_y_route[tmp_n+a[1]-a[0]-1])
    print(cob_list[min_id][point_n-1]-1)
    final_route_x.append(p_x_route[cob_list[min_id][point_n-1]-1])
    final_route_y.append(p_y_route[cob_list[min_id][point_n-1]-1])




def final_route(n,map_size,gasa_x,gasa_y):
    for i in range(n):
        for j in range(len(final_route_x[i])):
            final_r.append([(final_route_x[i][j]+gasa_x)*960/map_size,(final_route_y[i][j]+gasa_y)*960/map_size])




def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    #取得座標を格納する二次元配列
    s=[]
    Point_origin = []
    solve_flag = 0
    f_cnt = 0    
    Snow_Img = pygame.image.load("factory1.png").convert_alpha()
    Cloud_Img = pygame.image.load("tower2.png").convert_alpha()
    fps_clock = pygame.time.Clock()
    framerate = 500
    point_n = 0
    #testHome
    pygame.display.set_caption("MURAI NAVI")
    font = pygame.font.Font(None,55)
    one=pygame.image.load("one1.png").convert_alpha()
    two=pygame.image.load("two1.png").convert_alpha()
    three= pygame.image.load("three1.png").convert_alpha()
    four=pygame.image.load("four1.png").convert_alpha()
    five=pygame.image.load("five1.png").convert_alpha()
    six=pygame.image.load("six1.png").convert_alpha()
    seven=pygame.image.load("seven1.png").convert_alpha()
    eight=pygame.image.load("eight1.png").convert_alpha()
    nine=pygame.image.load("nine1.png").convert_alpha()
    x,y = (0,0)
    one_x,one_y = (-8,40)
    two_x,two_y = (302,40)
    three_x,three_y = (611,40)
    four_x,four_y = (-10,341)
    five_x,five_y = (302,340)
    six_x,six_y = (612,346)
    seven_x,seven_y = (-8,651)
    eight_x,eight_y = (302,640)
    nine_x,nine_y = (612,640)
    push = 0
    map_number = 0
    points_number = 4
    #screen.fill((0,20,0))
    #testHome
    Now_state = Map_select
    linegasa_x,linegasa_y = (0,0)
    dronegasa_x,dronegasa_y = (0,0)
    startgasa_x,startgasa_y =(0,0)
    pointgasa_x,pointgasa_y = (0,0)
    
    while (1):
        if Now_state == Map_select:
            screen.fill((20,0,0))
            text = font.render("Pick a map number and push",True,(255,255,255))
            screen.blit(text,[0,0])
            screen.blit(one,(one_x,one_y))
            screen.blit(two,(two_x,two_y))
            screen.blit(three,(three_x,three_y))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    if 0<(x-one_x)<one.get_height() and 0<(y-one_y)<one.get_width():
                        Now_state = Point_select
                        map_number = 1
                    if 0<(x-two_x)<two.get_height() and 0<(y-two_y)<two.get_width():
                        Now_state = Point_select
                        map_number = 2
                    if 0<(x-three_x)<three.get_height() and 0<(y-three_y)<three.get_width():
                        Now_state = Point_select
                        map_number = 3
            pygame.time.wait(10)
            
            
        if Now_state == Point_select:
            screen.fill((0,0,20))
            text = font.render("Pick a number of points and push",True,(255,255,255))
            screen.blit(text,[0,0])
            if map_number==1:
                Drone_Img = pygame.image.load("drone1.png").convert_alpha()
                
                grass_Img=load_img("grass.jpg")
                Map2.imgs[0] = pygame.transform.smoothscale(grass_Img,(48,48))       # 草地 map変更時変更
                stoon_Img=load_img("stoon.jpg")
                Map2.imgs[1] = pygame.transform.smoothscale(stoon_Img,(48,48))        # 岩 map変更時変更
                stoon2_Img=load_img("上半円.jpg")
                Map2.imgs[2] = pygame.transform.smoothscale(stoon2_Img,(48,48))                     
                stoon3_Img=load_img("右半円.jpg")
                Map2.imgs[3] = pygame.transform.smoothscale(stoon3_Img,(48,48))                     
                stoon4_Img=load_img("下半円.jpg")
                Map2.imgs[4] = pygame.transform.smoothscale(stoon4_Img,(48,48))                     
                stoon5_Img=load_img("左半円.jpg")
                Map2.imgs[5] = pygame.transform.smoothscale(stoon5_Img,(48,48)) 
                    
                stoon6_Img=load_img("右上.jpg")
                Map2.imgs[6] = pygame.transform.smoothscale(stoon6_Img,(48,48)) 
                    
                stoon7_Img=load_img("右下.jpg")
                Map2.imgs[7] = pygame.transform.smoothscale(stoon7_Img,(48,48)) 
                    
                stoon8_Img=load_img("左下.jpg")
                Map2.imgs[8] = pygame.transform.smoothscale(stoon8_Img,(48,48)) 
                    
                stoon9_Img=load_img("左上.jpg")
                Map2.imgs[9] = pygame.transform.smoothscale(stoon9_Img,(48,48))
                    
                stoon10_Img=load_img("map.jpg")
                Map2.imgs[10] = pygame.transform.smoothscale(stoon10_Img,(48,48)) 
                                
                
                
                
                
                map = Map1() #map変更時変更
                map_size = len(Map1.map) #map変更時変更
                linegasa_x,linegasa_y = (0.5,0.5)
                dronegasa_x,dronegasa_y = (25,25)
                startgasa_x,startgasa_y =(30,30)
                pointgasa_x,pointgasa_y = (25,25)
            elif map_number==2:
                Drone_Img = pygame.image.load("drone2.png").convert_alpha()
                
                
                grass_Img=load_img("grass.jpg")
                Map2.imgs[0] = pygame.transform.smoothscale(grass_Img,(48,48))       # 草地 map変更時変更
                stoon_Img=load_img("stoon.jpg")
                Map2.imgs[1] = pygame.transform.smoothscale(stoon_Img,(48,48))        # 岩 map変更時変更
                stoon2_Img=load_img("上半円.jpg")
                Map2.imgs[2] = pygame.transform.smoothscale(stoon2_Img,(48,48))                     
                stoon3_Img=load_img("右半円.jpg")
                Map2.imgs[3] = pygame.transform.smoothscale(stoon3_Img,(48,48))                     
                stoon4_Img=load_img("下半円.jpg")
                Map2.imgs[4] = pygame.transform.smoothscale(stoon4_Img,(48,48))                     
                stoon5_Img=load_img("左半円.jpg")
                Map2.imgs[5] = pygame.transform.smoothscale(stoon5_Img,(48,48)) 
                    
                stoon6_Img=load_img("右上.jpg")
                Map2.imgs[6] = pygame.transform.smoothscale(stoon6_Img,(48,48)) 
                    
                stoon7_Img=load_img("右下.jpg")
                Map2.imgs[7] = pygame.transform.smoothscale(stoon7_Img,(48,48)) 
                    
                stoon8_Img=load_img("左下.jpg")
                Map2.imgs[8] = pygame.transform.smoothscale(stoon8_Img,(48,48)) 
                    
                stoon9_Img=load_img("左上.jpg")
                Map2.imgs[9] = pygame.transform.smoothscale(stoon9_Img,(48,48))
                    
                stoon10_Img=load_img("map.jpg")
                Map2.imgs[10] = pygame.transform.smoothscale(stoon10_Img,(48,48)) 
                
                
                
                map = Map2() #map変更時変更
                map_size = len(Map2.map) #map変更時変更
                linegasa_x,linegasa_y = (0.5,0.5)
                dronegasa_x,dronegasa_y = (12,12)
                startgasa_x,startgasa_y =(30,30)
                pointgasa_x,pointgasa_y = (25,25)
            else:
                Drone_Img = pygame.image.load("drone2.png").convert_alpha()
                grass_Img = load_img("grass.jpg")
                Map3.imgs[0] = pygame.transform.smoothscale(grass_Img,(24,24))         # 草地 map変更時変更
                map_Img = load_img("map.jpg")
                Map3.imgs[1] = pygame.transform.smoothscale(map_Img,(24,24))
                map = Map3() #map変更時変更
                map_size = len(Map3.map) #map変更時変
                linegasa_x,linegasa_y = (0.5,0.5)
                dronegasa_x,dronegasa_y = (12,12)
                startgasa_x,startgasa_y =(30,30)
                pointgasa_x,pointgasa_y = (25,25)
            """
            screen.blit(two,(two_x,two_y))
            """
            screen.blit(three,(three_x,three_y))
            screen.blit(four,(four_x,four_y))
            screen.blit(five,(five_x,five_y))
            screen.blit(six,(six_x,six_y))
            screen.blit(seven,(seven_x,seven_y))
            screen.blit(eight,(eight_x,eight_y))
            screen.blit(nine,(nine_x,nine_y))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    """
                    if 0<(x-two_x)<two.get_height() and 0<(y-two_y)<two.get_width():
                        points_number = 2
                        Now_state = Play_pre
                    """
                    if 0<(x-three_x)<three.get_height() and 0<(y-three_y)<three.get_width():
                        points_number = 3
                        Now_state = Play_pre
                    if 0<(x-four_x)<four.get_height() and 0<(y-four_y)<four.get_width():
                        points_number = 4
                        Now_state = Play_pre
                    if 0<(x-five_x)<five.get_height() and 0<(y-five_y)<five.get_width():
                        points_number = 5
                        Now_state = Play_pre
                    if 0<(x-six_x)<six.get_height() and 0<(y-six_y)<six.get_width():
                        points_number = 6
                        Now_state = Play_pre
                    if 0<(x-seven_x)<seven.get_height() and 0<(y-seven_y)<seven.get_width():
                        points_number = 7
                        Now_state = Play_pre
                    if 0<(x-eight_x)<eight.get_height() and 0<(y-eight_y)<eight.get_width():
                        points_number = 8
                        Now_state = Play_pre
                    if 0<(x-nine_x)<nine.get_height() and 0<(y-nine_y)<nine.get_width():
                        points_number = 9
                        Now_state = Play_pre
            pygame.time.wait(10)
            
            
        if Now_state == Play_pre:
            point_n = points_number
            map.draw(screen)
            pygame.display.update()
            Now_state = Play
            
            
        if Now_state == Play:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    Point_origin.append([int(x),int(y)])
                    x = x/960*map_size 
                    y = y/960*map_size
                    s.append([x,y])
                    print(x,y)
            if len(s)==point_n:
                if solve_flag == 0:
                    p_and_cost = [[0 for i in range(point_n)] for j in range(point_n)] #実践プロ(都道府県間の距離のcsvファイル)と同じ感じで点々間のコスト入るよ
                    line_n = int(((point_n)*(point_n-1))/2) #すべての地点間に線を引いた時の本数
                    p_x_route = []*line_n
                    p_y_route = []*line_n
                    for i in range(point_n):
                        for j in range(i+1,point_n):
                            print(i,j)
                            if map_number==1:
                                p_and_cost[i][j] = solve(s[i],s[j],Map1.map,d_size,p_x_route,p_y_route) #map変更時変更
                            elif map_number==2:
                                p_and_cost[i][j] = solve(s[i],s[j],Map2.map,d_size,p_x_route,p_y_route) #map変更時変更
                            else:
                                p_and_cost[i][j] = solve(s[i],s[j],Map3.map,d_size,p_x_route,p_y_route) #map変更時変更
                            p_and_cost[j][i] = p_and_cost[i][j]
                    sale(p_and_cost,p_x_route,p_y_route,point_n) #セールスマン巡回
                    final_route(point_n,map_size,linegasa_x,linegasa_y)
                    print(final_r)
                    solve_flag +=1
                if f_cnt == (len(final_r)-1):
                    f_cnt = 0
                    map.draw(screen)
                map.draw(screen)
                for i in range(len(final_r)-1):
                    pygame.draw.lines(screen,(0,0,0),True,[final_r[i],final_r[i+1]],5)
                for i in range(len(Point_origin)):
                    if i==0:
                        screen.blit(Snow_Img,(Point_origin[i][0]-startgasa_x,Point_origin[i][1]-startgasa_y))
                    else:
                        screen.blit(Cloud_Img,(Point_origin[i][0]-pointgasa_x,Point_origin[i][1]-pointgasa_x))
                    screen.blit(Drone_Img,(final_r[f_cnt][0]-dronegasa_x,final_r[f_cnt][1]-dronegasa_y))
                f_cnt += 1
            fps_clock.tick(framerate)
            pygame.time.wait(200)
            # 終了用のイベント処理
        if event.type == QUIT: 
            print("smole_s=")
            print(s)
            # 閉じるボタンが押されたとき
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:       # キーを押したとき
            if event.key == K_ESCAPE:   # Escキーが押されたとき
                pygame.quit()
                sys.exit()
                
                
if __name__ == "__main__":
    main()    