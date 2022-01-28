class Ladder(object):
    def __init__(self):
        self.cross_layout = [[0, 0, 0], [1, 0, 2], [0, 0, 0], [0, 3, 0],
                             [0, 0, 0], [4, 0, 5], [0, 0, 0]]
        cross_info = dict()
        # breakable user color.
        cross_info[1] = (1, "system", "black")
        cross_info[2] = (1, "system", "black")
        cross_info[3] = (0, "system", "red")
        cross_info[4] = (1, "system", "black")
        cross_info[5] = (1, "system", "black")
        self.cross_info = cross_info
        self.cross_count = 5

    def __repr__(self):
        s = []
        for index, row in enumerate(self.cross_layout):
            s.append(str(index))
            s.append(": ")
            for cross in row:
                if cross:
                    s.append(str(self.cross_info[cross]))
                else:
                    s.append("(                    )")
            s.append("\n")
        return "".join(s)

    def sanity_check(self, row, column):
        if not isinstance(row, int):
            return False
        if not (0 <= row < len(self.cross_layout)):
            return False
        if not isinstance(column, int):
            return False
        if not (0 <= column < 3):
            return False
        return True

    def delete(self, row, column):
        if not self.sanity_check(row, column):
            return
        cross = self.cross_layout[row][column]
        if self.cross_info[cross][column]:
            self.cross_layout[row][column] = 0
        if self.cross_layout[row] == [0, 0, 0]:
            if self.cross_layout[row + 1] == [0, 0, 0]:
                del self.cross_layout[row + 1]
            if self.cross_layout[row - 1] == [0, 0, 0]:
                del self.cross_layout[row - 1]

    def append(self, row, column, user):
        if not self.sanity_check(row, column):
            return
        check_self = self.cross_layout[row][column] == 0
        check_left = column - 1 < 0 or self.cross_layout[row][column - 1] == 0
        check_right = column + 1 > 2 or self.cross_layout[row][column + 1] == 0

        if check_self and check_left and check_right:
            cross_id = self.cross_count + 1
            self.cross_info[cross_id] = (1, user, "black")
            self.cross_layout[row][column] = cross_id
            self.cross_count = cross_id
            if row == len(self.cross_layout) - 1 or self.cross_layout[
                    row + 1] != [0, 0, 0]:
                self.cross_layout.insert(row + 1, [0, 0, 0])
            if row == 0 or self.cross_layout[row - 1] != [0, 0, 0]:
                self.cross_layout.insert(row, [0, 0, 0])


def test_delete():
    ladder = Ladder()
    print(ladder)
    ladder.delete(5, 0)
    print(ladder)
    ladder.delete(5, 2)
    print(ladder)
    ladder.delete(1, 2)
    print(ladder)
    ladder.delete(1, 0)
    print(ladder)


if __name__ == "__main__":
    ladder = Ladder()
    print(ladder)
    ladder.append(0, 0, "illava")
    print(ladder)
    ladder.append(8, 1, "illava")
    print(ladder)
    ladder.append(6, 0, "frank")
    print(ladder)