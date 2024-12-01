from typing import List, Set, Dict, Tuple, Optional, Union, Iterable
import logging
import math
import structlog
from dataclasses import dataclass
from itertools import cycle
from enum import Enum, StrEnum
from shapely.geometry import Point, LineString, Polygon, LinearRing
import shapely

logger = structlog.get_logger()

@dataclass
class Cube:
    id: int
    start: Point
    end: Point
    color: Optional[str] = None

    def __hash__(self):
        return hash(self.id)

    def eight_corners(self):
        return [
            self.A,
            self.B,
            self.C,
            self.D,
            self.H,
            self.G,
            self.E,
            self.F,
        ]

    def eigth_faces(self):
        return [
            self.base_plane_points,
            self.top_plane_points,
            self.near_plane_points,
            self.far_plane_points,
            self.left_plane_points,
            self.right_plane_points,
        ]


    def as_polygon(self):
        return Polygon(self.eight_corners())


    @property
    def far_corner(self):
        x2 = self.end.x
        y2 = self.end.y
        z2 = self.end.z
        xx = x2 + 1
        yy = y2 + 1
        zz = z2 + 1
        return Point(xx, yy, zz)

    @property
    def A(self) -> Point:
        return self.start

    @property
    def B(self) -> Point:
        (x, y, z) = self.start.x, self.start.y, self.start.z
        (xx, yy, zz) = self.far_corner.x, self.far_corner.y, self.far_corner.z
        return Point(x, y, zz)

    @property
    def C(self) -> Point:
        (x, y, z) = self.start.x, self.start.y, self.start.z
        (xx, yy, zz) = self.far_corner.x, self.far_corner.y, self.far_corner.z
        return Point(xx, y, zz)

    @property
    def D(self) -> Point:
        (x, y, z) = self.start.x, self.start.y, self.start.z
        (xx, yy, zz) = self.far_corner.x, self.far_corner.y, self.far_corner.z
        return Point(xx, y, z)

    @property
    def E(self) -> Point:
        (x, y, z) = self.start.x, self.start.y, self.start.z
        (xx, yy, zz) = self.far_corner.x, self.far_corner.y, self.far_corner.z
        return Point(x, yy, z)

    @property
    def F(self) -> Point:
        (x, y, z) = self.start.x, self.start.y, self.start.z
        (xx, yy, zz) = self.far_corner.x, self.far_corner.y, self.far_corner.z
        return Point(x, yy, zz)

    @property
    def G(self) -> Point:
        return self.far_corner

    @property
    def H(self) -> Point:
        (x, y, z) = self.start.x, self.start.y, self.start.z
        (xx, yy, zz) = self.far_corner.x, self.far_corner.y, self.far_corner.z
        return Point(xx, yy, z)
    
    @property
    def base_plane_points(self):
        return [
            self.A,
            self.E,
            self.H,
            self.D,
        ]

    def scale_base_plane_points(self, scale: float):
        centroid = self.top_plane.centroid
        a_diff = centroid - self.A
        a_diff_point = Point((1-scale) * a_diff.x + self.A.x, (1-scale) * a_diff.y + self.A.y, self.A.z)
        e_diff = centroid - self.E
        e_diff_point = Point((1-scale) * e_diff.x + self.E.x, (1-scale) * e_diff.y + self.E.y, self.E.z)
        h_diff = centroid - self.H
        h_diff_point = Point((1-scale) * h_diff.x + self.H.x, (1-scale) * h_diff.y + self.H.y, self.H.z)
        d_diff = centroid - self.D
        d_diff_point = Point((1-scale) * d_diff.x + self.D.x, (1-scale) * d_diff.y + self.D.y, self.D.z)
        return [
            a_diff_point,
            e_diff_point,
            h_diff_point,
            d_diff_point,
        ]

    @property
    def base_plane(self):
        return Polygon(self.base_plane_points)

    @property
    def top_plane_points(self):
        return [
            self.B,
            self.F,
            self.G,
            self.C,
        ]

    def scale_top_plane_points(self, scale: float):
        centroid = self.top_plane.centroid
        norm = abs(centroid.distance(self.B)) * (1-scale)

        b_diff_point = Point(self.B.x + norm, self.B.y + norm, self.B.z)
        f_diff_point = Point(self.F.x + norm, self.F.y - norm, self.F.z)
        g_diff_point = Point(self.G.x - norm, self.G.y - norm, self.G.z)
        c_diff_point = Point(self.C.x - norm, self.C.y + norm, self.C.z)
        return [
            b_diff_point,
            f_diff_point,
            g_diff_point,
            c_diff_point,
        ]
        centroid = self.top_plane.centroid
        b_diff = centroid - self.B
        b_diff_point = Point((1-scale) * b_diff.x + self.B.x, (1-scale) * b_diff.y + self.B.y, self.B.z)
        f_diff = centroid - self.F
        f_diff_point = Point((1-scale) * f_diff.x + self.F.x, (1-scale) * f_diff.y + self.F.y, self.F.z)
        g_diff = centroid - self.G
        g_diff_point = Point((1-scale) * g_diff.x + self.G.x, (1-scale) * g_diff.y + self.G.y, self.G.z)
        c_diff = centroid - self.C
        c_diff_point = Point((1-scale) * c_diff.x + self.C.x, (1-scale) * c_diff.y + self.C.y, self.C.z)
        return [
            b_diff_point,
            f_diff_point,
            g_diff_point,
            c_diff_point,
        ]

    @property
    def top_plane(self):
        return Polygon(self.top_plane_points)

    @property
    def near_plane_points(self):
        return [
            self.A,
            self.B,
            self.C,
            self.D,
        ]
    @property
    def near_plane(self):
        return Polygon(self.near_plane_points)


    @property
    def far_plane_points(self):
        return [
            self.E,
            self.F,
            self.G,
            self.H,
        ]

    @property
    def far_plane(self):
        return Polygon(self.far_plane_points)

    @property
    def left_plane_points(self):
        return [
            self.A,
            self.B,
            self.F,
            self.E,
        ]

    @property
    def left_plane(self):
        return Polygon(self.left_plane_points)

    @property
    def right_plane_points(self):
        return [
            self.C,
            self.D,
            self.H,
            self.G,
        ]

    @property
    def right_plane(self):
        return Polygon(self.right_plane_points)


    def can_desintegrate(self, cubes: List["Cube"]) -> bool:
        if self.id == 0:
            return False
        for cube in cubes:
            if cube.id == self.id:
                continue
            # if cube is only supported by this cube, it can't desintegrate
            cubes_supporting_cube = cube.find_supporting_cubes(cubes)
            if len(cubes_supporting_cube) == 1:
                print("id", self.id)
                print("sel.color", self.color)
                print("cube.id", cube.id)
                print("cube.color", cube.color)
                assert cubes_supporting_cube[0].id == self.id
                return False
        return True

    def find_supporting_cubes(self, cubes: List["Cube"]) -> List["Cube"]:
        """Find all cubes that support this cube"""
        supporting_cubes = []
        for cube in cubes:
            if cube.id == self.id:
                continue
            if self.is_supported_by(cube):
                supporting_cubes.append(cube)
        return supporting_cubes

    def is_supported_by(self, other: "Cube") -> bool:
        """Is self cube supported by other cube?"""
        # if self cube is above other cube
        distance_z = other.end.z - self.start.z
        if not distance_z == 0:
            return False
        # need to be touching as well as intersecting heights
        return other.as_polygon().touches(self.as_polygon()) 

    def is_intersected_by_infinite_xy_plane(self, plane_z: int) -> bool:
        top_z = self.far_corner.z
        bottom_z = self.start.z
        return plane_z <= top_z and plane_z >= bottom_z

    def intersects_plane(self, plane: Polygon) -> bool:
        top_z = int(self.far_corner.z)
        bottom_z = int(self.start.z)
        # points_to_test = plane.exterior.coords
        # filter(lambda p: p.z >= bottom_z and p.z <= top_z, map(lambda c: Point(c), points_to_test))
        z_points = []
        top_plane_points = self.top_plane
        scaled_down_top_plane_points = self.scale_top_plane_points(.9)
        for z in range(top_z, bottom_z, -1):
            current_plane_points = []
            for point in scaled_down_top_plane_points:
                current_plane_points.append(Point(point.x, point.y, z))
            current_plane = LinearRing(current_plane_points)
            if current_plane.intersects(plane):
                return True
        return False
        

    def intersects(self, other: "Cube") -> bool:
        """Does self cube intersect with other cube?"""
        # if self top plane intersects other cube or other top plane intersects self cube
        other_top_plane = other.top_plane
        self_top_plane = self.top_plane

        return self.intersects_plane(other_top_plane) or other.intersects_plane(self_top_plane)


def plot_cubes(cubes: List[Cube], max_x: int, max_y: int, max_z: int, planes : List[Point] = []):
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import matplotlib.pyplot as plt
    import numpy as np
    from itertools import cycle
    colors = plt.cm.rainbow(np.linspace(0, 1, len(cubes)))
    colors = cycle(colors)

    fig = plt.figure()
    # ax = Axes3D(fig, auto_add_to_figure=False)
    ax = fig.add_subplot(111, projection='3d')
    fig.add_axes(ax)
    for plane in planes:
        x = list(map(lambda c: c.x, plane))
        y = list(map(lambda c: c.y, plane))
        z = list(map(lambda c: c.z, plane))
        verts = [list(zip(x,y,z))]
        ax.add_collection3d(Poly3DCollection(verts, color="black"))
    for cube in cubes:
        if cube.color is not None:
            color = cube.color
        else:
            color = next(colors)
            cube.color = color
        for face in cube.eigth_faces():
            x = list(map(lambda c: c.x, face))
            y = list(map(lambda c: c.y, face))
            z = list(map(lambda c: c.z, face))
            verts = [list(zip(x,y,z))]
            ax.add_collection3d(Poly3DCollection(verts, color=color))
        # corners = cube.eight_corners()
        # print(cube.start)
        # print(cube.end)
        # print(cube.far_corner)
        # print(corners)
        # x = list(map(lambda c: c.x, corners))
        # y = list(map(lambda c: c.y, corners))
        # z = list(map(lambda c: c.z, corners))
        # print(x)
        # print(y)
        # print(z)

        # # x = [0,1,1,0]
        # # y = [0,0,1,1]
        # # z = [0,1,0,1]
        # verts = [list(zip(x,y,z))]
        # ax.add_collection3d(Poly3DCollection(verts))
        # print(cube.id)
        # print(cube.start)
        # print(cube.end)
        # print(verts)
    plt.show()


def settle_cubes(cubes: List[Cube], max_x: int, max_y: int, max_z: int) -> Set[Cube]:
    moved_cubes = set()
    for z in range(max_z):
        cubes_to_move = set()
        print(f"z being checked: {z}")
        o = Point(0, 0, z)
        o1 = Point(max_x, 0, z)
        o2 = Point(0, max_y, z)
        o3 = Point(max_x, max_y, z)
        plane_points = [o, o1, o3, o2]
        plane = Polygon(plane_points)
        for cube in cubes:
            if cube not in moved_cubes:
                print(f"testing cube{cube} with {plane}", )
                # plot_cubes([cube], max_x, max_y, max_z, planes=[plane_points])
                if cube.is_intersected_by_infinite_xy_plane(z):
                    supporting_cubes = cube.find_supporting_cubes(cubes)
                    if len(supporting_cubes) == 0:
                        cubes_to_move.add(cube)
        print("cubes_to_move", cubes_to_move)
        for cube in cubes_to_move:
            moved_cubes.add(cube)
            starting_z = int(cube.start.z)
            no_supporting_cube_found = False
            for cube_z in range(starting_z, 0, -1):
                print("curent_z", cube_z)
                for other_cube in cubes:
                    if other_cube.id == cube.id:
                        continue
                    if other_cube.start.z > cube_z:
                        continue
                    intersecting = cube.intersects(other_cube)
                    scaled_down_top_plane_points = other_cube.scale_top_plane_points(.9)
                    print("intersecting", intersecting)
                    plot_cubes([cube, other_cube], max_x, max_y, max_z, planes=[scaled_down_top_plane_points])

                    if intersecting:
                        # found supporting cube
                        print("found supporting cube")
                        print(other_cube)
                        print("current_z", cube_z)
                        diff = cube_z - cube.start.z
                        print("supporting cube start z", other_cube.start.z)
                        print("supporting cube end z", other_cube.end.z)
                        print("supporting cube far end z", other_cube.far_corner.z)
                        print("current_start_z", cube.start.z)
                        print("current_end_z", cube.end.z)
                        print("diff", cube_z)
                        # plot_cubes([cube, other_cube], max_x, max_y, max_z, planes=[scaled_down_top_plane_points])
                        cube.start = Point(cube.start.x, cube.start.y, cube.start.z + diff)
                        cube.end = Point(cube.end.x, cube.end.y, cube.end.z + diff)
                        print("after_start_z", cube.start.z)
                        print("after_end_z", cube.end.z)
                        # cube.start.z += diff
                        # cube.end.z += diff
                        break
                else:
                    no_supporting_cube_found = True
            if no_supporting_cube_found:
                print("no supporting cube found", cube)
                # no supporting cube found, move to ground
                diff = - starting_z
                cube.start = Point(cube.start.x, cube.start.y, cube.start.z + diff)
                cube.end = Point(cube.end.x, cube.end.y, cube.end.z + diff)
            plot_cubes(cubes, max_x, max_y, max_z)

    return moved_cubes


def part1(values_list) -> str:
    # from structlog import get_logger
    # logger = get_logger()
    # logger.debug("part")
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    # structlog.contextvars.bind_contextvars(
    #     iteration=i,
    # )
#     data = """1,0,1~1,2,1
# 0,0,2~2,0,2
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9"""
    result = []
    cubes = []
    for i, values in enumerate(values_list):
        start, end = values.split("~")
        start = tuple(map(int, start.split(",")))
        end = tuple(map(int, end.split(",")))
        cube = Cube(
            id=i,
            start=Point(start),
            end=Point(end),
        )
        cubes.append(cube)
    max_x = int(max(map(lambda c: c.far_corner.x, cubes)))
    max_y = int(max(map(lambda c: c.far_corner.y, cubes)))
    max_z = int(max(map(lambda c: c.far_corner.z, cubes)))
    plot_cubes(cubes, max_x, max_y, max_z)

    # assert no cubes intersect
    # for cube in cubes:
    #     for other_cube in cubes:
    #         if cube.id == other_cube.id:
    #             continue
    #         print(cube)
    #         print(other_cube)
    #         assert not cube.as_polygon().intersects(other_cube.as_polygon())
    while True:
        change = settle_cubes(cubes, max_x, max_y, max_z)
        if not change:
            break
        plot_cubes(cubes, max_x, max_y, max_z)
    desintegratable_cubes = list(filter(lambda c: c.can_desintegrate(cubes), cubes))
    print(desintegratable_cubes)
    result = len(desintegratable_cubes)
    print(result)
    return f"{result}"
