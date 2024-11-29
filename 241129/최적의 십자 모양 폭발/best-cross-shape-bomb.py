# 구상
# N x N 크기 격자판
# 완탐 + 중력 + 두 방향 탐색
# BFS 를 할 때에는 기준점에서 오른쪽, 아래쪽만 본다. 2개가 되면 한 묶음 - 끝

def oob(row, col):
    return row < 0 or row >= N or col < 0 or col >= N


def find_twos(arr):
    count = 0
    for r in range(N):
        for c in range(N):
            if arr[r][c] == 0:
                continue
            current = arr[r][c]
            for d in range(2):      # 오른쪽, 아래쪽만 본다.
                nr = r + dr[d]
                nc = c + dc[d]
                if oob(nr, nc) or arr[nr][nc] != current:
                    continue
                count += 1

    return count


# 중력 메서드
def gravity(arr):
    for c in range(N):
        pointer = 0
        for r in reversed(range(N)):
            if arr[r][c] == 0:
                pointer += 1
            else:
                tmp = arr[r][c]
                arr[r][c] = 0
                arr[r + pointer][c] = tmp

    return arr


# 하나 골라서 터뜨리고, 중력 적용하고 배열 리턴한다.
def explode(arr):
    maximum = 0
    for r in range(N):
        for c in range(N):
            tmp_arr = [row[:] for row in arr]
            current = arr[r][c]
            tmp_arr[r][c] = 0       # 터짐 처리 (비운다)
            # 일단 십자 모양으로 터진다.
            for d in range(4):
                cr, cc = r, c
                for i in range(current - 1):
                    nr = cr + dr[d]
                    nc = cc + dc[d]
                    cr, cc = nr, nc
                    if oob(nr, nc):
                        break
                    tmp_arr[nr][nc] = 0
            # 이제 중력 작용한다.
            tmp_arr = gravity(tmp_arr)

            # 이제 조건 만족하는 쌍의 개수 찾는다.
            pair = find_twos(tmp_arr)
            maximum = max(maximum, pair)

    return maximum


N = int(input())
grid = []
for _ in range(N):
    grid.append(list(map(int, input().split())))

# delta 는 2 방향만 체크한다. - 오른쪽, 아래쪽 / 위쪽, 왼쪽
dr = [0, 1, -1, 0]
dc = [1, 0, 0, -1]

# << Unit Test >>
# grid = gravity(grid)
# print(*grid, sep='\n')

ans = explode(grid)
print(ans)