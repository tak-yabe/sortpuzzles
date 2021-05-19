#初期データ
A=10
B=11
C=12
"""now = [
   [1, 2, 3, 4], #1本目
   [5, 4, 6, 6],
   [7, 8, 1, 3],
   [5, 4, 9, 8],
   [A, 7, B, 7], #5本目
   [9, 4, 5, 3],
   [B, 5, 2, A], #7本目
   [A, B, 6, 9],
   [8, 9, 3, A],
   [C, 1, C, C], #10本目
   [1, 6, B, 8],
   [C, 7, 2, 2], #12本目
   [0, 0, 0, 0],
   [0, 0, 0, 0]
]"""
#チェックが苦しいので別のよりかんたんな問題から。
now = [
    [1, 2, 3, 4],
    [3, 5, 6, 3],
    [2, 7, 8, 4],
    [9, 4, 9, 6],
    [9, 8, 5, 5],
    [1, 7, 7, 6],
    [2, 1, 2, 9],
    [6, 8, 8, 1],
    [5, 3, 7, 4],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]


orig_occupy = []
for i in now:
   orig_occupy.append(i[:])

def check_send(lst):
   """
   底から情報が並んでいるlstからsend側の色と長さを抽出する。
   """
   moves = []
   c = 0
   for i in reversed(lst):
       #上からの情報を抽出。0(空)と単色の情報のみ抽出。
       if c == 0 or c == i:
           #上方が空、さもなくば観測された色と次のマスが同色のとき。
           moves.append(i)
           c = i #色を記録。空でもそのまま。
       else:
           #単色が観測されてて次の色が変わっているとき。
           break

   # send側の出力を決定。空の部分を外して色と長さを抽出。
   move_list = list(i for i in moves if i != 0)
   move_length = len(move_list)
   move_color = 0 #無色のボトルが選ばれたときの対策。
   if move_list:
       move_color = move_list[0]
   ## print(move_list, move_color, move_length)#確認用
   return move_color, move_length

def check_receive(lst):
   """
   底から情報が並んでいるlstからreceive側の長さ(余白)を抽出する。
   """
   capacity = 0
   for i in reversed(lst):
       #上から空の長さを抽出。
       if i == 0:
           capacity += 1
       else: #単色が観測されたとき。
           break

   # receive側の余白を抽出。
   if capacity == 4:
       color = 0
   else:
       color = lst[-capacity-1]
   return color, capacity

def main_move_judge(send, receive):
   """
   send側の移動がreceive側のキャパに適合するかチェックし、適・不適を判断する。
   """
   tf = False
   ind = -1
   cap = 0
   clr, lng = check_send(now[send])
   if lng:
       #移動対象があるとき、処理を続ける。
       typ, cap = check_receive(now[receive])
       if typ == 0:
           typ = clr #空のボトルがreceiveで選択されているとき、必ず受け入れられる。
       # sendとreceiveが同色で移動長さ(lng)以上にcapが大きいときは更新
       if clr == typ and lng <= cap:
           #更新すべき部分を抽出。
           ## TODO: トップではなく飛んだ先の底のを拾う挙動を修正。
           ## 修正方法：：行末のインデックスを[0]→[-1]に。あくまで上の方(順序で後ろ)を取得したいので。
           ind = list(k for k in range(5-lng) if now[send][k:k+lng] == [clr]*lng)[-1]
           tf = True
   return tf, ind, clr, lng, cap

def move(ind, clr, lng, cap, send, receive):
   #実際の更新操作
   for i in range(lng):
       now[send][ind+i] = 0 #移ったあとは空になる。
       now[receive][-cap+i] = clr #余白のうち底の方から移動する色になる。

def print_now(now):
   for i in now:
       print(i)
   print()

def check_movable():
   able = []
   for i in range(len(now)-1):
       for j in range(i+1,len(now)):
           tf, ind, clr, lng, cap = main_move_judge(i, j)
           if tf:
               able.append((i,j))
           tf, ind, clr, lng, cap = main_move_judge(j, i)
           if tf:
               able.append((j,i))
   return able

def check_complete():
    """
    移動完了の判定を行う。
    """
    tf = False
    if now == orig_occupy:
        return tf
    #else:下記の合否判定の処理に移る。
    for i in now:
        clr, nmb = check_send(i)
        if nmb != 4 and nmb != 0:
            break
    else:
        tf = True
    return tf

def move_from_able(movable_index):
    #check_movable関数の結果から指定の組の交換を行う。
    s, r = able[movable_index]
    tf, ind, clr, lng, cap = main_move_judge(s, r)
    if tf:
        move(ind, clr, lng, cap, s, r)

#以下の処理経路を自動で探索させたい。
able = check_movable()
print(check_complete())
move_from_able(1)
move_from_able(5)
move_from_able(17)

able = check_movable()
print(check_complete())
move_from_able(4)
move_from_able(6)

able = check_movable()
print(check_complete())
move_from_able(0)
move_from_able(2)

able = check_movable()
print(check_complete())
move_from_able(1)

able = check_movable()
print(check_complete())
move_from_able(1)

able = check_movable()
print(check_complete())
move_from_able(2)

able = check_movable()
print(check_complete())
move_from_able(1)

able = check_movable()
print(check_complete())
move_from_able(1)

able = check_movable()
print(check_complete())
move_from_able(1)

able = check_movable()
print(check_complete())
move_from_able(1)
move_from_able(11)

able = check_movable()
print(check_complete())
move_from_able(3)

able = check_movable()
print(check_complete())
move_from_able(2)

able = check_movable()
print(check_complete())
move_from_able(2)

able = check_movable()
print(check_complete())
move_from_able(0)
move_from_able(7)

able = check_movable()
print(check_complete())
move_from_able(1)
move_from_able(2)

able = check_movable()
print(check_complete())
move_from_able(1)

able = check_movable()
print(check_complete())
move_from_able(5)

able = check_movable()
print(check_complete())
move_from_able(1)

able = check_movable()
print(check_complete())
move_from_able(6)

able = check_movable()
print(check_complete())
move_from_able(0)
move_from_able(1)

able = check_movable()
print(check_complete())
move_from_able(2)

able = check_movable()
print(check_complete())
move_from_able(2)


#print_now(now)
print(check_complete())
#able = check_movable()
#for s,r in able:
#   print(s,r)
