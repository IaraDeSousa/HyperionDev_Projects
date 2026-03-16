def minesweeper(list: list[list[str]]):
    for i, row in enumerate(list):
        for k, col in enumerate(list):
            count = 0
            if(list[i][k] == "#"):
                continue
            if(list[i][k] == "-"):
                if(list[i-1][k-1] == "#" and i != 0 and k != 0):
                    count += 1
                if(list[i-1][k] == "#" and i != 0):
                    count += 1
                if(i !=0 and k != len(list[k]) - 1 and list[i-1][k+1] == "#" ):
                    count += 1
                if(k!= 0 and  list[i][k-1] == "#"):
                    count += 1
                if(k != len(list[k]) - 1 and list[i][k+1] == "#"):
                    count += 1
                if(i != len(list[i]) - 1 and k != 0 and list[i+1][k-1] == "#"):
                    count += 1
                if(i != len(list[i]) - 1 and list[i+1][k] == "#"):
                    count += 1
                if(i != len(list[i]) - 1 and k != len(list[k]) - 1 and list[i+1][k+1] == "#"):
                    count += 1
                list[i][k] = count

    for i, row in enumerate(list):
        print(*row, sep=" ")
    

list = [ ["-", "-", "-", "#", "#"], 
  ["-", "#", "-", "-", "-"], 
  ["-", "-", "#", "-", "-"], 
  ["-", "#", "#", "-", "-"], 
  ["-", "-", "-", "-", "-"] ]

minesweeper(list=list)

