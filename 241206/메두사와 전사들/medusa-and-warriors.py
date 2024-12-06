# 구상
# 메두사는 딱히 그리드에 표현하지 않을 것이다.
# 전사들은 각각을 하나의 객체로 보지 않을 것이다. 하나로 합쳐지면 결국 둘 이상이 같은 행동을 하기 때문이다.

from collections import deque


def oob(row, col):
    return row < 0 or row >= N or col < 0 or col >= N


def verti_oob(row):
    return row < 0 or row >= N


def paral_oob(col):
    return col < 0 or col >= N


# 최단 경로 BFS - 맨해튼 거리와 착각하면 안 된다.
def bfs(arr):       # arr는 도로 정보가 담겨 있는 grid
    visited = [[0 for _ in range(N)] for _ in range(N)]
    queue = deque()
    step = 1

    visited[sr][sc] = 1
    queue.append((sr, sc, [(sr, sc)]))      # 경로 정보도 함께 저장한다.

    while queue:
        step += 1
        for _ in range(len(queue)):
            cr, cc, path = queue.popleft()
            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]
                if oob(nr, nc) or visited[nr][nc] > 0 or arr[nr][nc] == 1:
                    continue
                visited[nr][nc] = 1
                queue.append((nr, nc, path + [(nr, nc)]))
                if nr == er and nc == ec:
                    path += [(nr, nc)]
                    return True, path[1]      # 최단 경로의 바로 다음 경로

    # 메두사의 집으로부터 공원까지 도달하는 경로가 없을 수도 있음을 유의하세요.
    return False, (-1, -1)


# 메두사의 이동 메서드
# 한 칸 이동이 단위이다.
def medusa_move(arr, w_arr):
    global sr, sc
    arrived = False
    possible, nxt = bfs(arr)
    # 만약 경로 없으면 그냥 종료한다.
    if not possible:
        return False, arrived, w_arr
    sr, sc = nxt
    # 메두사가 이동한 칸에 전사가 있을 경우 전사는 메두사에게 공격을 받고 사라집니다.
    if w_arr[sr][sc] > 0:
        w_arr[sr][sc] = 0       # 사망 처리. 따로 카운트할 필요 없다. 어디서도 요구하지 않기 때문이다.
    # 메두사가 공원에 도착하는 턴에는 0을 출력하고 프로그램을 종료합니다.
    if sr == er and sc == ec:
        arrived = True

    return True, arrived, w_arr


# 메두사의 시선 메서드
def medusa_stare(w_arr):
    # 메두사의 시야 범위 안에 들어오는 것들을 전부 담는다.
    # 상 하 좌 우 중 하나의 방향을 봐야 하므로, 우선 4번 순회를 한다.
    # 돌이 된 전사는 -1 을 곱해둔다.

    nomi_lst = []

    # 상 방향 - 좌상 & 우상
    for d in range(4):
        visited = [[0 for _ in range(N)] for _ in range(N)]
        stoned = 0
        stoned_lst = []     # 돌이 된 전사 (행, 열) 좌표를 담아놓는 리스트
        if d == 0 or d == 1:
            lcr, lcc = sr, sc       # 임의로 left, right 로 구분했다. 상, 하 방향이면 (왼쪽 ~ 오른쪽), 좌, 우 방향이면 (위 ~ 아래) 순이다.
            rcr, rcc = sr, sc
            while True:
                lnr = lcr + diag_dr[d][0]
                lnc = lcc + diag_dc[d][0]
                lcr, lcc = lnr, lnc
                rnr = rcr + diag_dr[d][1]
                rnc = rcc + diag_dc[d][1]
                rcr, rcc = rnr, rnc
                if verti_oob(lnr):
                    break
                left = max(0, lnc)
                right = min(N - 1, rnc)
                # 이제 순회를 돌면서 체크한다.
                for i in range(left, right + 1):
                    # 3 이면 그냥 continue 한다.
                    cr, cc = lnr, i
                    if visited[cr][cc] == 3:
                        continue
                    if w_arr[cr][cc] == 0:
                        visited[cr][cc] = 1
                    else:
                        visited[cr][cc] = 2
                        stoned += w_arr[cr][cc]
                        stoned_lst.append((cr, cc))

                        # 이 위치를 기준으로 퍼진다.
                        if cc == sc:    # 수직으로 같은 선에 있으면
                            while True:
                                nr = cr + dr[d]
                                nc = cc + dc[d]
                                cr, cc = nr, nc
                                if verti_oob(nr):
                                    break
                                visited[nr][nc] = 3
                        elif cc < sc:   # 왼쪽에 있으면
                            startc = cc
                            wcr, wcc = cr, cc
                            while True:
                                nr = wcr + diag_dr[d][0]
                                nc = wcc + diag_dc[d][0]
                                wcr, wcc = nr, nc
                                if verti_oob(nr):
                                    break
                                tmp_left = max(0, nc)
                                for j in range(tmp_left, startc + 1):
                                    visited[nr][j] = 3
                        elif cc > sc:   # 오른쪽에 있으면
                            startc = cc
                            wcr, wcc = cr, cc
                            while True:
                                nr = wcr + diag_dr[d][1]
                                nc = wcc + diag_dc[d][1]
                                wcr, wcc = nr, nc
                                if verti_oob(nr):
                                    break
                                tmp_right = min(N - 1, nc)
                                for j in range(startc, tmp_right + 1):
                                    visited[nr][j] = 3

        elif d == 2 or d == 3:      # 좌 우 방향에 대해 처리
            tcr, tcc = sr, sc   # top, bottom
            bcr, bcc = sr, sc
            while True:
                tnr = tcr + diag_dr[d][0]
                tnc = tcc + diag_dc[d][0]
                tcr, tcc = tnr, tnc
                bnr = bcr + diag_dr[d][1]
                bnc = bcc + diag_dc[d][1]
                bcr, bcc = bnr, bnc
                if paral_oob(tnc):
                    break
                top = max(0, tnr)
                bottom = min(N - 1, bnr)
                # 순회 돌면서 체크한다.
                for i in range(top, bottom + 1):
                    cr, cc = i, tnc
                    if visited[cr][cc] == 3:
                        continue
                    if w_arr[cr][cc] == 0:
                        visited[cr][cc] = 1
                    else:
                        visited[cr][cc] = 2
                        stoned += w_arr[cr][cc]
                        stoned_lst.append((cr, cc))

                        # 이 위치를 기준으로 퍼진다.
                        if cr == sr:        # 수평으로 같은 선에 있으면
                            while True:
                                nr = cr + dr[d]
                                nc = cc + dc[d]
                                cr, cc = nr, nc
                                if paral_oob(nc):
                                    break
                                visited[nr][nc] = 3
                        elif cr < sr:       # 위쪽에 있으면
                            startr = cr
                            wcr, wcc = cr, cc
                            while True:
                                nr = wcr + diag_dr[d][0]
                                nc = wcc + diag_dc[d][0]
                                wcr, wcc = nr, nc
                                if paral_oob(nc):
                                    break
                                tmp_top = max(0, nr)
                                for j in range(tmp_top, startr + 1):
                                    visited[j][nc] = 3
                        elif cr > sr:       # 아래쪽에 있으면
                            startr = cr
                            wcr, wcc = cr, cc
                            while True:
                                nr = wcr + diag_dr[d][1]
                                nc = wcc + diag_dc[d][1]
                                wcr, wcc = nr, nc
                                if paral_oob(nc):
                                    break
                                tmp_bottom = min(N - 1, nr)
                                for j in range(startr, tmp_bottom + 1):
                                    visited[j][nc] = 3

        nomi_lst.append((stoned, d, visited, stoned_lst))

    # 이제 nomi_lst 를 sort() 한다.
    nomi_lst.sort(key=lambda x: (-x[0], x[1]))
    elected = nomi_lst[0]
    # 이제 전사 그리드에 돌이 된 전사들 적용한다.
    for i in range(len(elected[3])):
        cr, cc = elected[3][i]
        w_arr[cr][cc] *= -1

    return elected[0], elected[2], w_arr


# 맨해튼 거리 구하는 메서드
def distance(wr, wc):
    return abs(wr - sr) + abs(wc - sc)


# 전사들 이동 & 공격 메서드
def warriors_charge(w_arr, visited):    # visited 는 위에서 받은 메두사의 시선
    # 돌로 변하지 않은 전사들은 메두사를 향해 최대 두 칸까지 이동합니다.
    # 전사들은 이동 중 같은 칸을 공유할 수 있습니다.
    # 동시 적용 고려해야 한다.
    tmp_arr = [[0 for _ in range(N)] for _ in range(N)]
    dead_warriors = 0
    moved_distance = 0
    strike_number = 0
    # 첫 번째 이동
    for r in range(N):
        for c in range(N):
            if w_arr[r][c] > 0:     # 돌이 되지 않은 전사들만
                first_move = False
                nxtr, nxtc = -1, -1
                cur_dist = distance(r, c)   # 현재 메두사와의 거리
                for d in range(4):
                    nr = r + dr[d]
                    nc = c + dc[d]
                    if oob(nr, nc) or visited[nr][nc] == 1 or visited[nr][nc] == 2 or distance(nr, nc) >= cur_dist:
                        continue
                    moved_distance += w_arr[r][c]
                    # 만약 전사가 메두사의 위치에 도달했다면,
                    if nr == sr and nc == sc:
                        dead_warriors += w_arr[r][c]
                        tmp_arr[r][c] -= w_arr[r][c]
                        strike_number += w_arr[r][c]
                        break
                    else:
                        # 가능한 게 있으면 바로 그 지점으로 정하고 break
                        first_move = True
                        # 그리드 업데이트를 위한 처리 한다.
                        tmp_arr[r][c] -= w_arr[r][c]
                        tmp_arr[nr][nc] += w_arr[r][c]
                        nxtr, nxtc = nr, nc
                        break
                if first_move:      # 처음 한 칸 이동했으면, 두 번째 움직임 시도해본다.
                    cur_dist = distance(nxtr, nxtc)
                    for d in range(4):
                        nr = nxtr + sdr[d]
                        nc = nxtc + sdc[d]
                        if oob(nr, nc) or visited[nr][nc] == 1 or visited[nr][nc] == 2 or distance(nr, nc) >= cur_dist:
                            continue
                        moved_distance += w_arr[r][c]
                        # 만약 전사가 메두사의 위치에 도달했다면
                        if nr == sr and nc == sc:
                            dead_warriors += w_arr[r][c]
                            tmp_arr[nxtr][nxtc] -= w_arr[r][c]
                            strike_number += w_arr[r][c]
                            break
                        else:
                            # 가능하면 그리드 업데이트를 위한 처리 한다.
                            tmp_arr[nxtr][nxtc] -= w_arr[r][c]
                            tmp_arr[nr][nc] += w_arr[r][c]
                            break
    # 이제 w_arr 최종 업데이트 해준다.
    for r in range(N):
        for c in range(N):
            w_arr[r][c] += tmp_arr[r][c]

    return w_arr, dead_warriors, moved_distance, strike_number


# 이번 턴이 종료되었을 때 돌에서 풀려납니다.
def release_spell(w_arr):
    for r in range(N):
        for c in range(N):
            if w_arr[r][c] < 0:
                w_arr[r][c] *= -1

    return w_arr


N, M = map(int, input().split())
sr, sc, er, ec = map(int, input().split())
warriors = []
data = list(map(int, input().split()))
warrior_grid = [[0 for _ in range(N)] for _ in range(N)]
for a in range(M):
    warriors.append((data[a * 2], data[a * 2 + 1]))
    warrior_grid[data[a * 2]][data[a * 2 + 1]] += 1     # 처음에 전사들의 입력이 다를 수도 있다는 말은 없으니..

grid = []
for _ in range(N):
    grid.append(list(map(int, input().split())))
# 도로는 0, 도로가 아닌 곳은 1

# 4 방향 delta - 상 하 좌 우 (우선순위 있음)
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

# 대각선 체크를 위한 delta - 상 하 좌 우 순으로
diag_dr = [
    [-1, -1],     # 상
    [1, 1],     # 하
    [-1, 1],     # 좌
    [-1, 1]      # 우
]
diag_dc = [
    [-1, 1],
    [-1, 1],
    [-1, -1],
    [1, 1]
]

# 좌우상하 delta
sdr = [0, 0, -1, 1]
sdc = [-1, 1, 0, 0]


# << Unit Test >>
# possible, nxt = bfs(grid)
# print(possible)
# print(nxt)
# flag, warrior_grid = medusa_move(grid, warrior_grid)
# print(flag)
# print(*warrior_grid, sep='\n')
# print(sr, sc)

# stoned_cnt, v, warrior_grid = medusa_stare(warrior_grid)
# print(stoned_cnt)
# print(*v, sep='\n')
# print('==================')
# print(*warrior_grid, sep='\n')
# print()
# warrior_grid, died = warriors_charge(warrior_grid, v)
# print(*warrior_grid, sep='\n')
# print(died)

while True:
    possible_flag, arrived_flag, warrior_grid = medusa_move(grid, warrior_grid)
    if not possible_flag:
        print(-1)
        break
    if arrived_flag:
        print(0)
        break
    stoned_cnt, v, warrior_grid = medusa_stare(warrior_grid)
    warrior_grid, died, moved_amount, strike_cnt = warriors_charge(warrior_grid, v)
    print(f'{moved_amount} {stoned_cnt} {strike_cnt}')
    warrior_grid = release_spell(warrior_grid)

