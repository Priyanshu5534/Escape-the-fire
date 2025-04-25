import streamlit as st
from collections import deque
import sys

# Directions: L R U D
dx = [0, 0, -1, 1]
dy = [-1, 1, 0, 0]

def update_fire_time(grid):
    m, n = len(grid), len(grid[0])
    fire_time = [[sys.maxsize] * n for _ in range(m)]
    visited = [[False] * n for _ in range(m)]
    q = deque()

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                fire_time[i][j] = 0
                visited[i][j] = True
                q.append((i, j))
            elif grid[i][j] == 2:
                fire_time[i][j] = -1

    curr_time = 0
    while q:
        curr_time += 1
        for _ in range(len(q)):
            x, y = q.popleft()
            for d in range(4):
                nx, ny = x + dx[d], y + dy[d]
                if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and fire_time[nx][ny] != -1:
                    fire_time[nx][ny] = curr_time
                    visited[nx][ny] = True
                    q.append((nx, ny))

    return fire_time

def is_possible(t, fire_time, grid):
    m, n = len(fire_time), len(fire_time[0])
    visited = [[False] * n for _ in range(m)]
    if fire_time[0][0] <= t:
        return False

    q = deque([(0, 0)])
    visited[0][0] = True
    curr_time = t

    while q:
        curr_time += 1
        for _ in range(len(q)):
            x, y = q.popleft()
            for d in range(4):
                nx, ny = x + dx[d], y + dy[d]
                if 0 <= nx < m and 0 <= ny < n and fire_time[nx][ny] != -1 and not visited[nx][ny]:
                    if nx == m - 1 and ny == n - 1 and curr_time <= fire_time[nx][ny]:
                        return True
                    if curr_time < fire_time[nx][ny]:
                        visited[nx][ny] = True
                        q.append((nx, ny))
    return False

def maximum_minutes(grid):
    m, n = len(grid), len(grid[0])
    fire_time = update_fire_time(grid)
    ans = -1
    left, right = 0, m * n + 1

    while left <= right:
        mid = (left + right) // 2
        if is_possible(mid, fire_time, grid):
            ans = mid
            left = mid + 1
        else:
            right = mid - 1

    return 1e9 if ans == m * n + 1 else ans

# Streamlit UI
st.title("🔥 Fire Escape Simulation")

st.markdown("""
**Legend:**
- `0` = Empty
- `1` = Fire
- `2` = Wall
""")

default_grid = "0 0 0\n2 2 0\n1 2 0\n0 2 0"

grid_input = st.text_area("Enter the grid (each row on new line):", default_grid)

if st.button("Calculate Maximum Wait Time"):
    try:
        grid = [list(map(int, row.strip().split())) for row in grid_input.strip().split("\n")]
        result = maximum_minutes(grid)
        st.success(f"✅ Maximum wait time: {int(result)}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

