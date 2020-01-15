import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

"""
    游戏逻辑控制器，负责处理游戏核心算法．
"""
import random


def restartmap():
    map = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    return map

class GameCoreController:
    def __init__(self):
        # 合并数据时使用的列表
        self.__list_merge = None
        # 生成新数字时使用的列表
        self.__list_empty_location = []

    def __zero_to_end(self):
        """
            零元素移动到末尾.
        """
        for i in range(-1, -len(self.__list_merge) - 1, -1):
            if self.__list_merge[i] == 0:
                del self.__list_merge[i]
                self.__list_merge.append(0)

    def __merge(self):
        """
            合并
        """
        self.__zero_to_end()
        score = 0
        for i in range(len(self.__list_merge) - 1):
            if self.__list_merge[i] == self.__list_merge[i + 1]:
                self.__list_merge[i] += self.__list_merge[i + 1]
                score += self.__list_merge[i]
                del self.__list_merge[i + 1]
                self.__list_merge.append(0)
        return score

    def move_left(self, map):
        """
            向左移动
        """
        score = 0
        for line in map:
            self.__list_merge = line
            score += self.__merge()
        return (map, score)

    def move_right(self, map):
        """
            向右移动
        """
        score = 0
        for line in map:
            self.__list_merge = line[::-1]
            score += self.__merge()
            line[::-1] = self.__list_merge
        return (map, score)

    def move_up(self, map):
        self.__square_matrix_transpose(map)
        map, score = self.move_left(map)
        self.__square_matrix_transpose(map)
        return (map, score)

    def move_down(self, map):
        self.__square_matrix_transpose(map)
        map, score = self.move_right(map)
        self.__square_matrix_transpose(map)
        return (map, score)

    def __square_matrix_transpose(self, map):
        """
            方阵转置
        :param sqr_matrix: 二维列表类型的方阵
        """
        for c in range(1, len(map)):
            for r in range(c, len(map)):
                map[r][c - 1], map[c - 1][r] = map[c - 1][r], map[r][c - 1]
        # return map

    def generate_number(self, map):
        """
            生成新数字
        """
        self.__get_empty_location(map)
        # 随机选择一个
        tuple_location = random.choice(self.__list_empty_location)
        number = self.__select_random_number()
        map[tuple_location[0]][tuple_location[1]] = number
        # 如果使用了该位置，就应该从列表中删除
        self.__list_empty_location.remove(tuple_location)
        return map

    def __select_random_number(self):
        """
            选择随机数字
        """
        return 4 if random.randint(1, 10) == 1 else 2

    def __get_empty_location(self, map):
        """
            找出所有空白位置
        :return:
        """
        # 计算前，先清空之前统计过的数据.
        self.__list_empty_location.clear()
        for r in range(len(map)):
            for c in range(len(map[0])):
                if map[r][c] == 0:
                    self.__list_empty_location.append((r, c))

    def is_game_over(self, map):
        """
            游戏是否结束
        """
        self.__get_empty_location(map)
        if len(self.__list_empty_location) > 0:
            return False

        for r in range(len(map)):  # 0
            for c in range(len(map[0]) - 1):  # 012
                if map[r][c] == map[r][c + 1] or map[c][r] == map[c + 1][r]:
                    return False
        return True


class GameConsoleView(View):
    concoller = GameCoreController()

    def post(self, request):
        # 根据输入移动地图
        data = json.loads(request.body)
        map = data['map']
        dir = data['dir']
        # 判断是否无效dir
        if dir == '?':
            result = {'code': 200, 'map': map, 'score': 0}
            return JsonResponse(result)
        map, score = self.__move_map_for_input(dir, map)
        # 判断游戏是否结束
        if self.concoller.is_game_over(map):
            result = {'code': 10001, 'error': "游戏结束", 'map': map, 'score': score}
            return JsonResponse(result)
        # 产生一个数字
        try:
            map = self.concoller.generate_number(map)
        except:
            result = {'code': 10002, 'error': "不能添加新元素,请尝试其他方向移动", 'map': map, 'score': score}
            return JsonResponse(result)
        result = {'code': 200, 'map': map, 'score': score}
        return JsonResponse(result)

    def __move_map_for_input(self, dir, map):
        if dir == "w":
            map, score = self.concoller.move_up(map)
        elif dir == "s":
            map, score = self.concoller.move_down(map)
        elif dir == "a":
            map, score = self.concoller.move_left(map)
        elif dir == "d":
            map, score = self.concoller.move_right(map)
        else:
            map = map
            score = 0
        return (map, score)


def mapview(request):
    return render(request, 'play/game2048.html', )


def initview(request):
    # map = NEWMAP
    # print('newmap=', map)
    map = restartmap()
    position = [x for x in range(15)]
    item1 = random.choice(position)
    position.remove(item1)
    item2 = random.choice(position)
    item1_x = item1 // 4
    item2_x = item2 // 4
    item1_y = item1 % 4
    item2_y = item2 % 4
    map[item1_x][item1_y] = 2
    map[item2_x][item2_y] = 2
    # 绘制界面
    result = {'code': 200, 'map': map}
    return JsonResponse(result)
