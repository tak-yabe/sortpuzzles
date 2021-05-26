#初期データ
A=10
B=11
C=12
now = [
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
]
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

def check_complete_orig():
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

def check_complete():
    """
    移動完了の判定を行う。
    """
    tf = False
    if now == orig_occupy:
        return tf
    #else:下記の合否判定の処理に移る。
    for i in now:
        #その瓶に全部一緒の色かどうかだけ見れば十分。
        clr = i[0]
        if i != [clr]*4 :
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

def move_from_index(send_index, receive_index):
    #指定の瓶同士の交換を行う。
    tf, ind, clr, lng, cap = main_move_judge(send_index, receive_index)
    if tf:
        move(ind, clr, lng, cap, send_index, receive_index)

def order_movement(n_lst, check = False):
    able = check_movable()
    for i in n_lst:
        send, receive = able[i]
        move_from_index(send, receive)
    """
    #just optional.
    if check:
        print(check_complete())
    """

def save_now(now):
    temp_occupy = []
    for i in now:
        temp_occupy.append(i[:])
    return temp_occupy

def load_temp(temp_occupy):
    for n,i in enumerate(temp_occupy):
        now[n] = i[:]
    return now

def check_next_movable(now, i):
    """
    仮に一つのオーダーを通した時に得られる配列から次のmovableを特定する。
    """
    temp = save_now(now) #調査時の配列を保存。
    # 保存しているうちにオーダーを出した場合のケーススタディを行う。
    order_movement([i])
    next_able = check_movable()
    now = load_temp(temp) #仮の更新なので配列を戻しておく。
    return next_able
    """
    #以下、旧版
    able = check_movable()
    next_candidates = []
    candidates = list(range(len(able)))
    for i in candidates:
        order_movement([i])
        able = check_movable()
        next_candidates.append((i,able))
        now = load_temp(temp)
    return next_candidates
    """

def orig_check_group(now):
    """
    #REVIEW: 消したい。一応消す前に記録残しておく。
    check_next関数の結果から元の遷移候補との差分を整理
    """
    plus = []
    same = []
    #minus = []
    able = check_movable()
    next_candidates = check_next(now)
    classified = []
    for i in next_candidates:
        for j in i[1]:
            if j in able:
                same.append(j)
            else:
                plus.append(j)
        """
        for j in able:
            if j not in i[1]:
                minus.append(j)
            else:
                pass #書くならsame.append(j)のイメージだが重複する。
        """
        print(len(same)  == len(list(set(same))))
        print(len(plus)  == len(list(set(plus))))
        same = list(set(same))
        plus = list(set(plus))
        #minus = list(set(minus))
        ###classified.append([same, plus, minus])
        classified.append([same, plus])
        break
    ###return classified
    return same, plus

def check_group(now, i):
    """
    check_next関数の結果から元の遷移候補との差分を整理
    """
    able = check_movable()
    next_able = check_next_movable(now, i)
    plus = []
    same = []
    for i in next_able:
        if i in able:
            same.append(i)
        else:
            plus.append(i)
    return same, plus

"""
自動化を目指してorder_movement関数に流すオーダーを作成する。
"""
### まずは等価な情報を判定して候補を減らす工夫をしないと苦しい。
#nowを一時保存しつつ中間物てきなnowから次の判定を行うとかを考える。
#どっかで終了判定も書く。
#終了判定もそうだが、等価配列の特定もしておきたい。ループ判定にも繋がる。
#ツリー化したい？→関数分けつつ。

able = check_movable()
for i in range(len(able)):
    same, plus = check_group(now, i)
    print(able[i])
    print(same)
    print(plus)
    print()

import time
tm = time.time()

#以下の処理経路を自動で探索させたい。
total_order = [
    [1,5,17], [4,6], [0,2], [1], [1], [2], [1],
    [1], [1], [1,11], [3], [2], [2], [0,7],
    [1,2], [1], [5], [1], [6], [1,0], [2], [2]
]

for i in total_order:
    order_movement(i, False)

print(time.time() - tm)

#print_now(now)
print(check_complete())
