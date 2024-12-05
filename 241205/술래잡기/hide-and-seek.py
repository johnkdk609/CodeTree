# 구상
# N x N 크기 격자
# 달팽이, 객체 관리 문제

def oob(row, col):
    return row < 0 or row >= N or col < 0 or col >= N


# 맨해튼 거리 찾는 메서드 (술래와의 거리)
def distance(x, y):
    return abs(x - sr) + abs(y - sc)


# 도망자들 도망치는 메서드
def runners_run(arr, lst):
    # arr 는 3차원 배열 grid, lst 는 도망자들 리스트인 runners
    # 술래와의 거리가 3 이하인 경우에만 움직일 수 있다.
    for i in range(M):
        if caught_runners[i] == 1:
            continue
        cnum, cr, cc, cur_d = lst[i]
        if distance(cr, cc) > 3:
            continue
        nr = cr + dr[cur_d]
        nc = cc + dc[cur_d]
        if oob(nr, nc):
            cur_d = (cur_d + 2) % 4
            nr = cr + dr[cur_d]
            nc = cc + dc[cur_d]
            if not (nr == sr and nc == sc):
                # 그리드 업데이트 한다.
                for j in range(len(arr[cr][cc])):
                    if arr[cr][cc][j][0] == cnum:
                        arr[cr][cc].pop(j)
                        break
                # 새 좌표에 넣는다.
                arr[nr][nc].append((cnum, nr, nc, cur_d))
                # 리스트 업데이트 한다.
                lst[i] = (cnum, nr, nc, cur_d)
            else:   # 방향 바꾸고 한 칸 갔는데 술래 있으면 그대로 있는다.
                # 방향 정보 업데이트 해줘야 한다.
                for j in range(len(arr[cr][cc])):
                    if arr[cr][cc][j][0] == cnum:
                        arr[cr][cc][j] = (cnum, cr, cc, cur_d)
                # 리스트도 업데이트 해준다.
                lst[i] = (cnum, cr, cc, cur_d)
        else:   # 격자 벗어나지 않는 경우
            # 움직이려는 칸에 술래가 있는 경우라면 움직이지 않습니다.
            # 이 경우에는 따로 코드 추가할 것이 없다. 아무것도 안 하면 되는 것이다.
            # 움직이려는 칸에 술래가 있지 않다면 해당 칸으로 이동합니다. 해당 칸에 나무가 있어도 괜찮습니다.
            if not (nr == sr and nc == sc):
                # 그리드 업데이트 한다.
                for j in range(len(arr[cr][cc])):
                    if arr[cr][cc][j][0] == cnum:
                        arr[cr][cc].pop(j)
                        break
                # 새로운 좌표에 넣어준다.
                arr[nr][nc].append((cnum, nr, nc, cur_d))
                # 리스트도 업데이트 해준다.
                lst[i] = (cnum, nr, nc, cur_d)

    return arr, lst


# 술래의 움직임 - 달팽이
def catcher_snail_move(visited):
    global sr, sc, s_dir, status
    if status == 1:     # 시계방향 확산 달팽이
        # 한 칸 전진하고 바로 오른쪽 꺾을 수 있는지 본다.
        nr = sr + dr[s_dir]
        nc = sc + dc[s_dir]
        sr, sc = nr, nc
        visited[nr][nc] = 1
        tmp_dir = (s_dir + 1) % 4
        tmp_r = nr + dr[tmp_dir]
        tmp_c = nc + dc[tmp_dir]
        if visited[tmp_r][tmp_c] == 0:      # 꺾을 수 있으면
            s_dir = tmp_dir

        # (0, 0) 에 도달했으면 바로 status 와 방향 정보 바꾼다.
        if sr == 0 and sc == 0:
            status = 2
            s_dir = 2   # 아래쪽 바라보게 한다.
            visited = [[0 for _ in range(N)] for _ in range(N)]
            visited[0][0] = 1

    else:       # 반시계방향 수렴 달팽이
        # 한 칸 전진하고, 한 번 더 전진할 수 있는지 본다.
        # 만약 한 번 더 전진할 수 없으면 좌회전 한다.
        nr = sr + dr[s_dir]
        nc = sc + dc[s_dir]
        sr, sc = nr, nc
        visited[nr][nc] = 1
        tmp_r = nr + dr[s_dir]
        tmp_c = nc + dc[s_dir]
        if oob(tmp_r, tmp_c) or visited[tmp_r][tmp_c] > 0:
            s_dir = (s_dir - 1) % 4

        # (N // 2, N // 2) 에 도달했으면 바로 status 와 방향 정보 바꾼다.
        if sr == N // 2 and sc == N // 2:
            status = 1
            s_dir = 0
            visited = [[0 for _ in range(N)] for _ in range(N)]
            visited[N // 2][N // 2] = 1

    return visited


# 술래의 시야 범위 (자기 포함 3) 안에 있는 도망자 잡는 메서드
# 나무 신경 써야 한다.
def catcher_catch(arr, turn):   # 점수 산정을 위한 turn
    cnt = 0
    for i in range(3):
        nr = sr + i * dr[s_dir]
        nc = sc + i * dc[s_dir]
        if oob(nr, nc):
            break
        if tree_grid[nr][nc] == 1:
            continue
        if len(arr[nr][nc]) > 0:    # 도망자가 있는 것
            for j in range(len(arr[nr][nc])):
                caught_runners[arr[nr][nc][j][0] - 1] = 1
                cnt += 1
            # 그리드 비운다. 리스트는 신경 쓸 필요 없다.
            arr[nr][nc] = []

    score = cnt * turn

    return arr, score


N, M, H, K = map(int, input().split())
runners = []
grid = [[[] for _ in range(N)] for _ in range(N)]

# 4 방향 delta - 상 우 하 좌
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

for m in range(M):
    a, b, d = map(int, input().split())
    a -= 1
    b -= 1      # 인덱스 처리
    if d == 1:      # 좌우 움직임. 오른쪽 보고 시작
        grid[a][b].append((m + 1, a, b, 1))     # 번호도 부여하겠다.
        runners.append((m + 1, a, b, 1))
    elif d == 2:
        grid[a][b].append((m + 1, a, b, 2))    # 아래쪽 보고 시작
        runners.append((m + 1, a, b, 2))

tree_grid = [[0 for _ in range(N)] for _ in range(N)]
for _ in range(H):
    a, b = map(int, input().split())
    a -= 1
    b -= 1      # 인덱스 처리
    tree_grid[a][b] = 1     # 나무가 있으면 1로 체크한다.

# 도망자끼리 위치가 겹쳐져 주어지는 경우는 없으며,
# 나무들 역시 위치가 겹쳐져 주어지는 경우는 없다고 가정해도 좋습니다.
# 단, 이동 도중 도망자들의 위치는 겹칠 수 있음에 유의합니다.

sr, sc = N // 2, N // 2     # 술래의 시작 위치
s_dir = 0       # 술래의 시작 방향 (위쪽)
status = 1      # 시계방향 확산 달팽이의 경우 status 를 1로, 반시계방향 수렴 달팽이의 경우 status 를 2로 한다.

v = [[0 for _ in range(N)] for _ in range(N)]
v[sr][sc] = 1

caught_runners = [0 for _ in range(M)]      # 잡히면 1로 체크한다.


# << Unit Test >>
# grid, runners = runners_run(grid, runners)
# print(*grid, sep='\n')
# print(runners)
# v = catcher_snail_move(v)
# print(*v, sep='\n')
# print(s_dir)
# print(sr, sc)

#########################################################################
# 출력
# 술래가 k번의 턴 동안 얻게되는 총 점수를 출력합니다.

total_score = 0
for k in range(K):
    grid, runners = runners_run(grid, runners)
    v = catcher_snail_move(v)
    grid, sco = catcher_catch(grid, k + 1)
    total_score += sco

print(total_score)

# dir_dict = {
#     0: '↑', 1: '→', 2: '↓', 3: '←'
# }
#
# print(f'시작 술래 위치: ({sr}, {sc})')
# print(f'시작 술래 방향: {dir_dict[s_dir]}')
# print()
# print('====================================')
#
# for a in range(60):
#     v = catcher_snail_move(v)
#     print(f'{a + 1} 번째')
#     for r_ in range(N):
#         for c_ in range(N):
#             print(f'{v[r_][c_]:<2}', end='')
#         print()
#     print(f'현재 술래 위치: ({sr}, {sc})')
#     print(f'현재 술래 방향: {dir_dict[s_dir]}')
#     print()
#     print('================================')
