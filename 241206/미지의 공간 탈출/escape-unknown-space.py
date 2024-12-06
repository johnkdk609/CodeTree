# 구상
# N x N -> 미지의 공간 크기
# M -> 시간의 벽의 한 변의 길이
# step BFS + 끝과 끝 연결하기

from collections import deque


def moob(row, col):     # 미지의 공간 경계 체크
    return row < 0 or row >= N or col < 0 or col >= N


def toob(row, col):     # 시간의 벽 경계 체크
    return row < 0 or row >= M or col < 0 or col >= M


def bfs(marr, tarr, lst):       # lst 는 시간 이상 현상 정보를 담은 리스트
    # 시간의 벽의 visited 배열과, 미지의 공간의 visited 배열을 전부 만든다.
    m_visited = [[0 for _ in range(N)] for _ in range(N)]
    t_visited = [[[0 for _ in range(M)] for _ in range(M)] for _ in range(5)]

    queue = deque()       # 큐는 하나로 관리한다.

    step = 1
    # 시작 지점 넣는다. 처음에는 시간의 벽 안에서 시작한다.
    t_visited[4][sr][sc] = step
    queue.append((4, sr, sc))     # 시간의 벽의 몇 번째 면인지 정보를 맨 앞에 둔다.
    # 미지의 공간은 5로 하겠다.

    # 일단 모든 시간 이상 현상에 대해 현재 칸을 -1 로 처리한다.
    for i in range(len(lst)):
        ri, ci, di, vi = lst[i]
        m_visited[ri][ci] = -1

    while queue:
        # 먼저 시간 이상 현상이 퍼진다. 시간 이상 현상은 -1 로 체크하겠다.
        for i in range(len(lst)):
            ri, ci, di, vi = lst[i]
            if step % vi == 0:
                nri = ri + dr[di]
                nci = ci + dc[di]
                if moob(nri, nci) or marr[nri][nci] == 1 or marr[nri][nci] == 4 or marr[nri][nci] == 3:
                    continue
                m_visited[nri][nci] = -1    # 한 칸 전진할 수 있는 상황
                # 리스트 업데이트 해줘야 한다.
                lst[i] = (nri, nci, di, vi)

        step += 1
        for _ in range(len(queue)):
            cdm, cr, cc = queue.popleft()       # current dimension
            # 현재 시간의 벽에 있는지, 아니면 미지의 공간에 있는지에 따라 상황이 달라진다.
            # if 0 <= cdm < 5:       # 시간의 벽에 있는 상황
            # 이제 4방 탐색 한다.
            for d in range(4):
                nr = cr + dr[d]
                nc = cc + dc[d]
                if cdm == 4:    # 윗면부터 처리하겠다.
                    if nr < 0:      # 위쪽으로 벗어나면 북쪽 면이다.
                        if t_visited[3][0][M - 1 - cc] > 0 or tarr[3][0][M - 1 - cc] == 1:      # 이미 방문했거나, 장애물이 있는 곳이면
                            continue
                        t_visited[3][0][M - 1 - cc] = step
                        queue.append((3, 0, M - 1 - cc))
                    elif nr >= M:   # 아래쪽으로 벗어나면 남쪽 면이다.
                        if t_visited[2][0][cc] > 0 or tarr[2][0][cc] == 1:
                            continue
                        t_visited[2][0][cc] = step
                        queue.append((2, 0, cc))
                    elif nc < 0:    # 왼쪽으로 벗어나면 서쪽 면이다.
                        if t_visited[1][0][cr] > 0 or tarr[1][0][cr] == 1:
                            continue
                        t_visited[1][0][cr] = step
                        queue.append((1, 0, cr))
                    elif nc >= M:   # 오른쪽으로 벗어나면 동쪽 면이다.
                        if t_visited[0][0][M - 1 - cr] > 0 or tarr[0][0][M - 1 - cr] == 1:
                            continue
                        t_visited[0][0][M - 1 - cr] = step
                        queue.append((0, 0, M - 1 - cr))
                    else:   # 윗면에서 경계 벗어나지 않게 움직인 경우
                        if t_visited[4][nr][nc] > 0 or tarr[4][nr][nc] == 1:
                            continue
                        t_visited[4][nr][nc] = step
                        queue.append((4, nr, nc))
                ###########################################################################################
                elif cdm == 0:  # 동쪽 면
                    if nr < 0:      # 위쪽으로 벗어나면 윗면이다.
                        if t_visited[4][M - 1 - cc][M - 1] > 0 or tarr[4][M - 1 - cc][M - 1] == 1:
                            continue
                        t_visited[4][M - 1 - cc][M - 1] = step
                        queue.append((4, M - 1 - cc, M - 1))
                    elif nc < 0:    # 왼쪽으로 벗어나면 남쪽 면이다.
                        if t_visited[2][cr][M - 1 - cc] > 0 or tarr[2][cr][M - 1 - cc] == 1:
                            continue
                        t_visited[2][cr][M - 1 - cc] = step
                        queue.append((2, cr, M - 1 - cc))
                    elif nc >= M:   # 오른쪽으로 벗어나면 북쪽 면이다.
                        if t_visited[3][cr][M - 1 - cc] > 0 or tarr[3][cr][M - 1 - cc] == 1:
                            continue
                        t_visited[3][cr][M - 1 - cc] = step
                        queue.append((3, cr, M - 1 - cc))
                    elif nr >= M:   # 아래쪽으로 벗어나면, 이제 탈출구를 찾아야 한다.
                        if cr == time_exit_r and cc == time_exit_c:
                            # 미지의 공간 체크를 한다.
                            # 나가자마자 막혀있을 수 있다는 점을 감안해야 한다.
                            # 나가자마자 탈출구가 있을 수 있다는 점을 감안해야 한다.
                            if m_visited[mys_entry_r][mys_entry_c] > 0:
                                continue
                            if marr[mys_entry_r][mys_entry_c] == 4:     # 탈출구이면 종료한다.
                                return step - 1
                            # 탈출구도 아니고 막혀있지도 않으면,
                            m_visited[mys_entry_r][mys_entry_c] = step
                            queue.append((5, mys_entry_r, mys_entry_c))
                    else:   # 동쪽 면에서 경계 벗어나지 않고 움직였을 때
                        if t_visited[0][nr][nc] > 0 or tarr[0][nr][nc] == 1:
                            continue
                        t_visited[0][nr][nc] = step
                        queue.append((0, nr, nc))
                ###########################################################################################
                elif cdm == 1:      # 서쪽 면
                    if nr < 0:      # 위쪽으로 벗어나면 위쪽 면이다.
                        if t_visited[4][cc][0] > 0 or tarr[4][cc][0] == 1:
                            continue
                        t_visited[4][cc][0] = step
                        queue.append((4, cc, 0))
                    elif nc < 0:    # 왼쪽으로 벗어나면 북쪽 면이다.
                        if t_visited[3][cr][M - 1 - cc] > 0 or tarr[3][cr][M - 1 - cc] == 1:
                            continue
                        t_visited[3][cr][M - 1 - cc] = step
                        queue.append((3, cr, M - 1 - cc))
                    elif nc >= M:   # 오른쪽으로 벗어나면 남쪽 면이다.
                        if t_visited[2][cr][M - 1 - cc] > 0 or tarr[2][cr][M - 1 - cc] == 1:
                            continue
                        t_visited[2][cr][M - 1 - cc] = step
                        queue.append((2, cr, M - 1 - cc))
                    elif nr >= M:   # 아래쪽으로 벗어나면 탈출구 찾아봐야 한다.
                        if cr == time_exit_r and cc == time_exit_c:
                            if m_visited[mys_entry_r][mys_entry_c] > 0:
                                continue
                            if marr[mys_entry_r][mys_entry_c] == 4:     # 탈출구이면 종료한다.
                                return step - 1
                            # 탈출구도 아니고 막혀있지도 않으면,
                            m_visited[mys_entry_r][mys_entry_c] = step
                            queue.append((5, mys_entry_r, mys_entry_c))
                    else:   # 서쪽 면에서 경계 벗어나지 않고 움직였을 때
                        if t_visited[1][nr][nc] > 0 or tarr[1][nr][nc] == 1:
                            continue
                        t_visited[1][nr][nc] = step
                        queue.append((1, nr, nc))
                ###########################################################################################
                elif cdm == 2:      # 남쪽 면
                    if nr < 0:      # 위쪽으로 벗어나면 윗면이다.
                        if t_visited[4][M - 1][cc] > 0 or tarr[4][M - 1][cc] == 1:
                            continue
                        t_visited[4][M - 1][cc] = step
                        queue.append((4, M - 1, cc))
                    elif nc < 0:    # 왼쪽으로 벗어나면 서쪽 면이다.
                        if t_visited[1][cr][M - 1 - cc] > 0 or tarr[1][cr][M - 1 - cc] == 1:
                            continue
                        t_visited[1][cr][M - 1 - cc] = step
                        queue.append((1, cr, M - 1 - cc))
                    elif nc >= M:   # 오른쪽으로 벗어나면 동쪽 면이다.
                        if t_visited[0][cr][M - 1 - cc] > 0 or tarr[0][cr][M - 1 - cc] == 1:
                            continue
                        t_visited[0][cr][M - 1 - cc] = step
                        queue.append((0, cr, M - 1 - cc))
                    elif nr >= M:   # 아래쪽으로 벗어나면 탈출구 찾아봐야 한다.
                        if cr == time_exit_r and cc == time_exit_c:
                            if m_visited[mys_entry_r][mys_entry_c] > 0:
                                continue
                            if marr[mys_entry_r][mys_entry_c] == 4:     # 탈출구이면 종료한다.
                                return step - 1
                            # 탈출구도 아니고 막혀있지도 않으면,
                            m_visited[mys_entry_r][mys_entry_c] = step
                            queue.append((5, mys_entry_r, mys_entry_c))
                    else:   # 남쪽 면에서 경계 벗어나지 않고 움직였을 때
                        if t_visited[2][nr][nc] > 0 or tarr[2][nr][nc] == 1:
                            continue
                        t_visited[2][nr][nc] = step
                        queue.append((2, nr, nc))
                ###########################################################################################
                elif cdm == 3:      # 북쪽 면
                    if nr < 0:      # 위쪽으로 벗어난 것이면 윗면이다.
                        if t_visited[4][0][M - 1 - cc] > 0 or tarr[4][0][M - 1 - cc] == 1:
                            continue
                        t_visited[4][0][M - 1 - cc] = step
                        queue.append((4, 0, M - 1 - cc))
                    elif nc < 0:    # 왼쪽으로 벗어난 것이면 동쪽 면이다.
                        if t_visited[0][cr][M - 1 - cc] > 0 or tarr[0][cr][M - 1 - cc] == 1:
                            continue
                        t_visited[0][cr][M - 1 - cc] = step
                        queue.append((0, cr, M - 1 - cc))
                    elif nc >= M:   # 오른쪽으로 벗어난 것이면 서쪽 면이다.
                        if t_visited[1][cr][M - 1 - cc] > 0 or tarr[1][cr][M - 1 - cc] == 1:
                            continue
                        t_visited[1][cr][M - 1 - cc] = step
                        queue.append((1, cr, M - 1 - cc))
                    elif nr >= M:   # 아래쪽으로 벗어나면, 탈출구 찾아봐야 한다.
                        if cr == time_exit_r and cc == time_exit_c:
                            if m_visited[mys_entry_r][mys_entry_c] > 0:
                                continue
                            if marr[mys_entry_r][mys_entry_c] == 4:     # 탈출구이면 종료한다.
                                return step - 1
                            # 탈출구도 아니고 막혀있지도 않으면,
                            m_visited[mys_entry_r][mys_entry_c] = step
                            queue.append((5, mys_entry_r, mys_entry_c))
                    else:   # 북쪽 면 경계 안에서 움직이고 있으면
                        if t_visited[3][nr][nc] > 0 or tarr[3][nr][nc] == 1:
                            continue
                        t_visited[3][nr][nc] = step
                        queue.append((3, nr, nc))
                ###########################################################################################
                elif cdm == 5:      # 미지의 공간 안에 있는 경우
                    if moob(nr, nc) or m_visited[nr][nc] > 0 or marr[nr][nc] == 1 or marr[nr][nc] == 3 or m_visited[nr][nc] == -1:
                        continue
                    m_visited[nr][nc] = step
                    queue.append((5, nr, nc))
                    # 탈출구 만나면 바로 종료한다.
                    # 탈출구가 한 개인지, 두 개 이상인지 얘기가 없으므로...
                    if marr[nr][nc] == 4:
                        return step - 1

    return -1


N, M, F = map(int, input().split())
grid = []
for _ in range(N):
    grid.append(list(map(int, input().split())))

time_grid = [
    [],     # 시간의 벽의 동
    [],     # 서
    [],     # 남
    [],     # 북
    []      # 윗면
]

for a in range(5):
    for b in range(M):
        time_grid[a].append(list(map(int, input().split())))

# 4 방향 delta - 동 서 남 북
dr = [0, 0, 1, -1]
dc = [1, -1, 0, 0]


strange_phenomenon = []
for _ in range(F):
    ri_, ci_, di_, vi_ = map(int, input().split())
    strange_phenomenon.append((ri_, ci_, di_, vi_))

# 시간의 벽에서 출발점 찾는다.
sr, sc = -1, -1
breaker = False
for a in range(M):
    if breaker:
        break
    for b in range(M):
        if time_grid[4][a][b] == 2:
            sr, sc = a, b
            breaker = True
            break

# 시간의 벽과 미지의 공간의 연결 통로 좌표를 찾는다.
# 미지의 공간 평면도에서 3을 기준으로 찾는다.
mys_entry_r, mys_entry_c = -1, -1
mys_entry_dir = -1
start3_flag = False
start3_r, start3_c = -1, -1
breaker = False
for a in range(N):
    if breaker:
        break
    for b in range(N):
        if breaker:
            break
        if grid[a][b] == 3:
            if not start3_flag:
                start3_r, start3_c = a, b
                start3_flag = True
            for d_ in range(4):
                na = a + dr[d_]
                nb = b + dc[d_]
                if moob(na, nb) or grid[na][nb] == 1 or grid[na][nb] == 3:
                    continue
                if grid[na][nb] == 0 or grid[na][nb] == 4:
                    mys_entry_r, mys_entry_c = na, nb
                    mys_entry_dir = d_
                    breaker = True
                    break

# dir_dict = {
#     0: '동', 1: '서', 2: '남', 3: '북'
# }
# print(f'미지의 공간 평면도에서 3과 바로 연결된 통로 좌표: ({mys_entry_r}, {mys_entry_c})')
# print(f'시간의 벽 중 어떤 면이 미지의 공간과 연결돼 있는가: {dir_dict[mys_entry_dir]}쪽 면')

# 시간의 벽에서 어떤 지점이 미지의 공간과 연결되는지 찾는다.
time_exit_dimension = mys_entry_dir
time_exit_r, time_exit_c = -1, -1
if time_exit_dimension == 0:        # 동쪽에 연결된 것이면
    r_diff = mys_entry_r - start3_r
    c_diff = mys_entry_c - 1 - start3_c
    time_exit_r, time_exit_c = M - 1, M - 1 - r_diff
elif time_exit_dimension == 1:      # 서쪽에 연결된 것이면
    r_diff = mys_entry_r - start3_r
    c_diff = mys_entry_c + 1 - start3_c
    time_exit_r, time_exit_c = M - 1, r_diff
elif time_exit_dimension == 2:      # 남쪽에 위치한 것이면
    r_diff = mys_entry_r - 1 - start3_r
    c_diff = mys_entry_c - start3_c
    time_exit_r, time_exit_c = M - 1, c_diff
elif time_exit_dimension == 3:      # 북쪽에 위치한 것이면
    r_diff = mys_entry_r + 1 - start3_r
    c_diff = mys_entry_c - start3_c
    time_exit_r, time_exit_c = M - 1, M - 1 - c_diff

# print(f'시간의 벽에서 탈출 면: {dir_dict[time_exit_dimension]} 쪽 방향')
# print(f'시간의 벽에서 탈출하는 곳 좌표: ({time_exit_r}, {time_exit_c})')

ans = bfs(grid, time_grid, strange_phenomenon)
print(ans)