MOD = 1000000007

def solve_matrix_path():
    first_line = input().strip().split()
    if not first_line:
        return
    n, m = int(first_line[0]), int(first_line[1])

    grid = []
    for _ in range(n):
        grid.append(input().strip().split())

    if grid[0][0] == 'X' or grid[n-1][m-1] == 'X':
        print("IMPOSSIBLE")
        return

    # dp[r][c] = (max_score, path_count)
    dp = [[(float('-inf'), 0)] * m for _ in range(n)]
    dp[0][0] = (int(grid[0][0]), 1)

    for r in range(n):
        for c in range(m):
            if grid[r][c] == 'X' or dp[r][c][0] == float('-inf'):
                continue

            curr_score, curr_ways = dp[r][c]

            # Moves: Right (r, c+1), Down (r+1, c), Diagonal (r+1, c+1)
            moves = [(r, c+1), (r+1, c), (r+1, c+1)]
            for nr, nc in moves:
                if nr < n and nc < m and grid[nr][nc] != 'X':
                    cell_val = int(grid[nr][nc])
                    new_score = curr_score + cell_val

                    existing_score, existing_ways = dp[nr][nc]

                    if new_score > existing_score:
                        dp[nr][nc] = (new_score, curr_ways)
                    elif new_score == existing_score:
                        dp[nr][nc] = (existing_score, (existing_ways + curr_ways) % MOD)

    max_score, ways = dp[n-1][m-1]
    if max_score == float('-inf'):
        print("IMPOSSIBLE")
    else:
        print(f"{max_score} {ways}")

if __name__ == "__main__":
    solve_matrix_path()
