"""
1차 풀이 - 12/01

수행 시간 : 343 ms
메모리 : 25 MB
시도 횟수 : 1

총 3시간 55분 소요 (09:00 ~ 12:55)
09:00 ~ 09:35 문제 분석 및 구상
09:36 ~ 12:30 구현
12:31 ~ 12:55 검증 및 제출 (맞았습니다)

[문제 정리 및 구상]
최단 경로 BFS, 시뮬레이션
'메두사의 시선' 부분에 대한 아이디어를 생각하는 데에 꽤 오랜 시간이 걸렸다.
방향에 대해 메두사 지점부터 쭉 퍼지면서 전사가 없으면 방문 체크 배열에 1, 전사가 나오면 방문 체크 배열에서 일단 해당 전사를 2로 바꾼다.
그리고 그 전사로부터 같은 방향으로 퍼지면서 그 전사의 시야에 의해 가려지는 부분들은 전부 3으로 체크한다.
그 이후에 전사가 나오더라도, 방문 체크 배열에 해당 칸이 3이므로 그냥 continue 한다.

[리뷰]
올해 기출 오후 문제를 이번에 처음 풀었다. 구현 속도가 여전히 좀 아쉽다. 더 빠르게 해야 한다.
"""


# 구상
# N x N 크기 마을
# 메두사의 집과 공원이 연결되지 않을 수도 있다. 그러면 -1 출력하면 됨.

# 일단, 메두사의 집과 공원이 연결되는지를 봐야 한다. 전사들과는 상관없다.
# 그냥 진짜 연결이 되어 있어야 함.

from collections import deque


def oob(row, col):
    return row < 0 or row >= N or col < 0 or col >= N


# 바로 다음 칸도 찾음과 동시에, '연결되어 있는지'를 파악할 것이다.
def path_bfs(arr, s_r, s_c, e_r, e_c):
    visited = [[0 for _ in range(N)] for _ in range(N)]
    queue = deque()
    visited[s_r][s_c] = 1
    queue.append((s_r, s_c, [(s_r, s_c)]))      # 경로도 함께 저장한다.

    step = 1

    while queue:
        step += 1
        for _ in range(len(queue)):
            cr, cc, path = queue.popleft()
            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]
                if oob(nr, nc) or visited[nr][nc] > 0 or arr[nr][nc] == 1:
                    continue
                visited[nr][nc] = step
                queue.append((nr, nc, path + [(nr, nc)]))
                if nr == e_r and nc == e_c:
                    path += [(nr, nc)]
                    return True, path[1]    # True 와 함께, 바로 다음 한 칸을 리턴한다.

    return False, (-1, -1)      # 집과 공원 연결 안 돼 있으면 그냥 False 리턴한다. (-1, -1) 은 더미 데이터.


# 메두사의 이동 메서드
def medusa_move(arr, w_arr):   # w_arr 는 전사들을 그리드에 표현한 warrior_grid
    global mr, mc
    arrived = False     # 도착 여부 체크를 위함
    impossible = False      # 아얘 메두사 집과 공원이 연결 안 된 경우
    # arr는 grid, lst 는 warriors
    # 일단 메두사 한 칸 이동한다.
    flag, nxt = path_bfs(arr, mr, mc, er, ec)
    mr, mc = nxt
    # 만약, 메두사의 집으로부터 공원까지 이어지는 도로가 존재하지 않는다면 -1을 출력합니다.
    if not flag:
        impossible = True
        return arr, w_arr, arrived, impossible    # 밖에서 만약 impossible 이 True 이면 그냥 -1 출력하고 종료한다.
    # 단, 메두사가 공원에 도착하면 0을 출력하고 프로그램을 종료합니다.
    if mr == er and mc == ec:
        arrived = True
        return arr, w_arr, arrived, impossible
    # 메두사가 이동한 칸에 전사가 있을 경우 전사는 메두사에게 공격을 받고 사라집니다.
    # '돌이 되었다' 는 표현이 없으므로, 그냥 이 죽은 전사들은 카운트하지 않는다.
    if w_arr[nxt[0]][nxt[1]] > 0:
        w_arr[nxt[0]][nxt[1]] = 0

    return arr, w_arr, arrived, impossible


# 메두사의 시선 메서드
# 메두사 기준 상-하-좌-우 방향을 전부 확인하고, 그 중 가장 많은 전사를 돌로 만드는 경우를 선택해야 한다.
def medusa_stare(w_arr):
    nomi_lst = []
    for d in range(4):
        # 4방 탐색을 하는데, 메두사 기준 해당 방향으로 대각선으로 퍼진다.
        # 양 대각선 사이에 (경계 포함) 있는 지점들 전부가 시야이다. 일단 방문 체크 배열을 1로 바꾼다.
        # 순회를 돌면서 해당 지점 안에 전사가 있으면 전사를 리스트에 담는데, 방문 체크 배열이 3이면 안 담는다.
        # 담으면서 2로 체크해둔다.
        # 그 전사를 기준으로 메두사 기준 어디인지 파악해 퍼져서 해당 지점은 3으로 바꾼다.
        visited = [[0 for _ in range(N)] for _ in range(N)]
        lcr, lcc = mr, mc
        rcr, rcc = mr, mc
        stoned_warrior = []
        while True:     # 이 반복문의 정체는? => 가능한 경우까지 전부 탐색하는 것
            lnr = lcr + mdr[d][0]
            lnc = lcc + mdc[d][0]
            lcr, lcc = lnr, lnc
            rnr = rcr + mdr[d][1]
            rnc = rcc + mdc[d][1]
            rcr, rcc = rnr, rnc
            # while 문 종료 조건 꼭 써야 한다!!
            if d == 0 and lcr < 0:
                break
            if d == 1 and lcr >= N:
                break
            if d == 2 and lcc < 0:
                break
            if d == 3 and lcc >= N:
                break

            if d == 0 or d == 1:    # 상, 하 이면 왼쪽 오른쪽만 보면 된다.
                for i in range(max(0, lcc), min(N - 1, rcc) + 1):
                    if visited[rcr][i] == 3:
                        continue
                    visited[rcr][i] = 1
                    # 만약 전사가 있으면
                    if w_arr[rcr][i] > 0 and visited[rcr][i] != 3:
                        # 이제 해당 전사를 기준으로 자신의 시야 방향에 있는 것들을 3으로 바꾼다.
                        visited[rcr][i] = 2
                        stoned_warrior.append((rcr, i))
                        # 만약 발각된 전사가 메두사와 같은 열에 있다면
                        if i == mc:
                            # 본인 기준 쭉 뒤만 3으로 바꾼다.
                            # d 방향 지표를 사용하면 된다.
                            w_cr, w_cc = rcr, i
                            while True:
                                w_nr = w_cr + dr[d]
                                w_nc = w_cc + dc[d]
                                w_cr, w_cc = w_nr, w_nc
                                if oob(w_cr, w_cc):
                                    break
                                visited[w_cr][w_cc] = 3
                        # 만약 발각된 전사가 메두사 열 기준 왼쪽 열에 있었다면
                        elif i < mc:
                            w_cr, w_cc = rcr, i
                            while True:
                                w_nlr = w_cr + mdr[d][0]
                                w_nlc = w_cc + mdc[d][0]
                                w_cr, w_cc = w_nlr, w_nlc
                                if oob(w_cr, i):      # 신중해야 한다.
                                    break
                                for j in range(max(0, w_cc), i + 1):
                                    visited[w_cr][j] = 3
                        # 만약 발각된 전사가 메두사 열 기준 오른쪽 열에 있었다면
                        elif i > mc:
                            w_cr, w_cc = rcr, i
                            while True:
                                w_nlr = w_cr + mdr[d][1]
                                w_nlc = w_cc + mdc[d][1]
                                w_cr, w_cc = w_nlr, w_nlc
                                if oob(w_cr, i):      # 신중해야 한다.
                                    break
                                for j in range(i, min(w_cc, N - 1) + 1):
                                    visited[w_cr][j] = 3
            # 좌, 우 방향도 본다.
            elif d == 2 or d == 3:      # 좌, 우 방향의 경우 위, 아래만 보면 된다.
                for i in range(max(0, lcr), min(N - 1, rcr) + 1):
                    if visited[i][lcc] == 3:
                        continue
                    visited[i][lcc] = 1
                    # 만약 전사가 있으면
                    if w_arr[i][lcc] > 0 and visited[i][lcc] != 3:
                        # 해당 전사 기준으로 자신의 시야 방향에 있는 것들을 3으로 바꾼다.
                        visited[i][lcc] = 2
                        stoned_warrior.append((i, lcc))
                        # 만약 발각된 전사가 메두사와 같은 행에 있다면
                        if i == mr:
                            w_cr, w_cc = i, lcc
                            while True:
                                w_nr = w_cr + dr[d]
                                w_nc = w_cc + dc[d]
                                w_cr, w_cc = w_nr, w_nc
                                if oob(i, w_cc):
                                    break
                                visited[w_cr][w_cc] = 3
                        # 만약 발각된 전사가 메두사 행 기준 위쪽 행에 있다면
                        elif i < mr:
                            w_cr, w_cc = i, rcc
                            while True:
                                w_nlr = w_cr + mdr[d][0]
                                w_nlc = w_cc + mdc[d][0]
                                w_cr, w_cc = w_nlr, w_nlc
                                if oob(mr, w_cc):
                                    break
                                for j in range(max(0, w_cr), i + 1):
                                    visited[j][w_cc] = 3
                        # 만약 발각된 전사가 메두사 행 기준 아래쪽 행에 있다면
                        elif i > mr:
                            w_cr, w_cc = i, rcc
                            while True:
                                w_nlr = w_cr + mdr[d][1]
                                w_nlc = w_cc + mdc[d][1]
                                w_cr, w_cc = w_nlr, w_nlc
                                if oob(mr, w_cc):
                                    break
                                for j in range(i, min(N - 1, w_cr) + 1):
                                    visited[j][w_cc] = 3

        # print(f'{d} 방향 visited 출력')
        # print(*visited, sep='\n')
        # print('돌이 된 전사들 리스트 출력:', stoned_warrior)
        # print('=======================================')

        # 한 칸에 두 명 이상의 전사가 있을 수도 있으니, 그것 감안해 넣어야 한다.
        tmp_total = 0
        for i in range(len(stoned_warrior)):
            tmp_r, tmp_c = stoned_warrior[i]
            tmp_total += w_arr[tmp_r][tmp_c]
        nomi_lst.append((tmp_total, d, stoned_warrior, visited))

    # 이제 선별한다.
    nomi_lst.sort(key=lambda x: (-x[0], x[1]))

    elected = nomi_lst[0]   # 선별된 것
    # 이제 돌로 될 전사들 돌로 바꾼다. 돌이 되는 것은 음수로 처리한다.

    elected_stoned = elected[2]
    for i in range(len(elected_stoned)):
        wr, wc = elected_stoned[i]
        w_arr[wr][wc] *= -1

    return w_arr, elected_stoned, elected[0], elected[3]    # 두 번째는 돌이 된 좌표, 세 번째 이번에 돌이 된 전사의 수, 마지막은 현재 메두사의 시선을 담은 배열


# 맨해튼 거리 찾는 메서드
def distance(c_r, c_c):
    return abs(c_r - mr) + abs(c_c - mc)


# 전사들 이동 & 공격 메서드 한꺼번에 작성한다.
# 맨해튼 거리로 두 번 이동한다.
def warriors_approach(w_arr, medusa_v):     # medusa_v 는 '메두사의 시선' 메서드 실행 후 얻는 '메두사의 시야 정보'가 담긴 배열이다.
    # 임시 배열을 생성해서 거기에 옮긴다.
    tmp_arr = [[0 for _ in range(N)] for _ in range(N)]
    strike_cnt = 0
    moved_distance = 0
    for r in range(N):
        for c in range(N):
            # 돌로 변한 전사들은 이동하지 못하니, continue 한다.
            if w_arr[r][c] < 0:
                continue
            elif w_arr[r][c] > 0:   # 이동할 수 있는 전사만
                cr, cc = r, c
                # 첫 번째 이동
                # 메두사와의 거리를 줄일 수 있는 방향으로 한 칸 이동합니다. 이런 방향이 두 개 이상일 경우 상하좌우의 우선순위로 방향을 선택합니다.
                # 격자의 바깥으로 나갈 수 없으며, 메두사의 시야에 들어오는 곳으로는 이동할 수 없습니다.
                cur_dist = distance(cr, cc)       # 현재 지점에서 메두사와의 거리
                first_move = False
                for d in range(4):
                    nr = cr + dr[d]
                    nc = cc + dc[d]
                    if oob(nr, nc) or medusa_v[nr][nc] == 1 or medusa_v[nr][nc] == 2 or distance(nr, nc) >= cur_dist:
                        continue
                    cr, cc = nr, nc
                    first_move = True
                    moved_distance += w_arr[r][c]
                    break       # 하나라도 나오면 그냥 종료한다.
                # 만약 한 번 움직였는데 메두사 지점으로 온 것이면, 메두사를 공격한 전사 수에 더한다.
                if first_move:
                    if cr == mr and cc == mc:
                        strike_cnt += w_arr[r][c]
                        tmp_arr[r][c] -= w_arr[r][c]
                    else:
                        tmp_arr[r][c] -= w_arr[r][c]
                        tmp_arr[cr][cc] += w_arr[r][c]
                        prev_r, prev_c = cr, cc     # 배열 업데이트를 위해 사용하는 임시 변수

                        # 여기서 두 번째 이동 시도한다.
                        cur_dist = distance(cr, cc)
                        second_move = False
                        for d in range(4):
                            nr = cr + sdr[d]
                            nc = cc + sdc[d]
                            if oob(nr, nc) or medusa_v[nr][nc] == 1 or medusa_v[nr][nc] == 2 or distance(nr, nc) >= cur_dist:
                                continue
                            cr, cc = nr, nc
                            second_move = True
                            moved_distance += w_arr[r][c]
                            break
                        if second_move:
                            if cr == mr and cc == mc:
                                strike_cnt += w_arr[r][c]
                                tmp_arr[prev_r][prev_c] -= w_arr[r][c]
                            else:
                                tmp_arr[prev_r][prev_c] -= w_arr[r][c]
                                tmp_arr[cr][cc] += w_arr[r][c]

    # 이제 전사들 좌표 최종 업데이트 한다.
    for r in range(N):
        for c in range(N):
            w_arr[r][c] += tmp_arr[r][c]

    return w_arr, strike_cnt, moved_distance


# 한 턴의 마지막에 모든 돌이 된 전사들 정상으로 돌려놔야 한다.
def release_spell(w_arr):
    for r in range(N):
        for c in range(N):
            if w_arr[r][c] < 0:
                w_arr[r][c] *= -1
    return w_arr


N, M = map(int, input().split())
sr, sc, er, ec = map(int, input().split())

# 전역 변수로 사용할 메두사의 좌표
mr, mc = sr, sc

warriors = []
warrior_grid = [[0 for _ in range(N)] for _ in range(N)]
data = list(map(int, input().split()))
for a in range(0, M * 2, 2):
    warriors.append((data[a], data[a + 1]))
    warrior_grid[data[a]][data[a + 1]] += 1

grid = []   # 마을 정보
for _ in range(N):
    grid.append(list(map(int, input().split())))

# 메두사의 이동 - 여러 최단 경로가 가능하다면 상, 하, 좌, 우의 우선순위를 따른다.
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]

# 좌우상하의 우선순위 - 아주 괘씸하다...
sdr = [0, 0, -1, 1]
sdc = [-1, 1, 0, 0]

# 메두사 시선 기준, 상하좌우 우선순위라면 각각 봐야 하는 지점들을 본다.
mdr = [
    [-1, -1],     # 좌상, 우상
    [1, 1],     # 좌하, 우하
    [-1, 1],     # 좌상, 좌하
    [-1, 1]      # 우상, 우하
]
mdc = [
    [-1, 1],
    [-1, 1],
    [-1, -1],
    [1, 1]
]

# << Unit Test >>
# flag, nxt = path_bfs(grid, sr, sc, er, ec)
# print(nxt)
# print(*warrior_grid, sep='\n')
# grid, warrior_grid, arrived_flag, impossible_flag = medusa_move(grid, warrior_grid)

# print(f'현재 메두사 좌표: ({mr}, {mc})')
# print('현재 그리드 출력')
# print(*grid, sep='\n')
# print('현재 전사들 그리드 출력')
# print(*warrior_grid, sep='\n')
# print('<<<<< 메두사 시선 메서드 실행!!! >>>>>')
# warrior_grid, stoned_coord, stoned_num, medusa_onsight = medusa_stare(warrior_grid)
# print(*warrior_grid, sep='\n')
# print('현재 돌이 된 전사들 좌표 출력:', stoned_coord)
# print('현재 돌이 된 전사들 수 출력:', stoned_num)
# print(*medusa_onsight, sep='\n')
# print()
# warrior_grid, strike_num = warriors_approach(warrior_grid, medusa_onsight)
# print(*warrior_grid, sep='\n')
# print(strike_num)


########################################################################
# 출력
# 각 턴마다 한 줄에 모든 전사가 이동한 거리의 합, 메두사로 인해 돌이 된 전사의 수,
# 메두사를 공격한 전사의 수를 공백을 사이에 두고 출력합니다.

# 단, 메두사가 공원에 도착하면 0을 출력하고 프로그램을 종료합니다.

# 만약, 메두사의 집으로부터 공원까지 이어지는 도로가 존재하지 않는다면 -1을 출력합니다.

turn = 1
while True:
    # print(f'@@@@@ {turn} 번째 턴 @@@@@')
    # print()
    # print('<<<<< 메두사 이동!! >>>>>')
    grid, warrior_grid, arrived_flag, impossible_flag = medusa_move(grid, warrior_grid)
    # print('메두사 이동한 후 전사 그리드 출력')
    # print(*warrior_grid, sep='\n')
    # print(f'현재 메두사 좌표: ({mr}, {mc})')
    if impossible_flag:
        # print('연결 안 되어 있으니 그냥 바로 종료 ~~!')
        print(-1)
        break
    if arrived_flag:
        # print('도착했으니 종료 ~~~!')
        print(0)
        break

    # print()
    # print('<<<<< 메두사 시선 메서드 실행 ㄷㄷㄷ >>>>')
    warrior_grid, stoned_coord, stoned_num, medusa_onsight = medusa_stare(warrior_grid)
    # print('전사 그리드 출력')
    # print(*warrior_grid, sep='\n')
    # print('이번 턴에 돌이 된 사람의 수:', stoned_num)
    # print('메두사의 시야 상태 출력')
    # print(*medusa_onsight, sep='\n')
    # print()
    # print('<<<<< 전사들 접근 및 공격 메서드 실행! >>>>>')
    warrior_grid, strike_num, total_moved_dist = warriors_approach(warrior_grid, medusa_onsight)
    # print('전사 그리드 출력')
    # print(*warrior_grid, sep='\n')
    # print('이번 턴에 메두사 타격한 수:', strike_num)
    # print('이번 턴에 이동한 전사들 총 이동거리:', total_moved_dist)
    # print()
    # print('<<<<< 석화 해제 메서드 실행 !! >>>>>')
    warrior_grid = release_spell(warrior_grid)      # 석화 해제
    # print('석화 해제된 후 전사 그리드 출력')
    # print(*warrior_grid, sep='\n')
    # print()
    # print('=============================================================================')
    print(f'{total_moved_dist} {stoned_num} {strike_num}')

    turn += 1