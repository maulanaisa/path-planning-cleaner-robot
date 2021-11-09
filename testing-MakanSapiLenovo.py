import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from random import randint
import math


#warna untuk peta
cmap = colors.ListedColormap(['white','blue','black','cyan'])

#kelas untuk objek robot
class peta :
    #current[row,column]
    current = np.array ([1,1])

    # 0 = utara, 1 = barat, 2 = selatan, 3 = timur
    direction = 0
    sensor_read = {'depan' : 0, 'belakang' : 0, 'kanan' : 0, 'kiri' : 0}
    sensor_read_before = {'depan' : 0, 'belakang' : 0, 'kanan' : 0, 'kiri' : 0}

    all_edges = np.empty((0,2,2),dtype = int)
    all_nodes = np.empty((0,2),dtype = int)
    black_grid = np.empty((0,2),dtype=int)
    submap = list()
    cleaned_submap = list()

    created_map = np.empty((0,0),dtype=int)

    obstacle = np.array ([
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],

    ])

    #perintah maju
    def moving(self) :
        if self.direction == 0 :
            self.current [0] = self.current[0] + 1
        elif self.direction == 2 :
            self.current [0] = self.current[0] - 1
        elif self.direction == 3 :
            self.current [1] = self.current[1] - 1
        elif self.direction == 1 :
            self.current [1] = self.current[1] + 1

    #fungsi pembacaan sensor 4 arah
    def sensor (self) :
        self.sensor_read_before = self.sensor_read.copy()
        if self.direction == 0 :
            self.sensor_read.update({'depan' : self.obstacle[self.current[0]+1,self.current[1]]})
            if self.sensor_read['depan'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0]+1,self.current[1]]],axis=0)

            self.sensor_read.update({'belakang' : self.obstacle[self.current[0]-1,self.current[1]]})
            #if self.sensor_read['belakang'] == 2 :
                #self.black_grid = np.append(self.black_grid,[[self.current[0]-1,self.current[1]]],axis=0)

            self.sensor_read.update({'kiri' : self.obstacle[self.current[0],self.current[1]+1]})
            if self.sensor_read['kiri'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0],self.current[1]+1]],axis=0)

            self.sensor_read.update({'kanan' : self.obstacle[self.current[0],self.current[1]-1]})
            if self.sensor_read['kanan'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0],self.current[1]-1]],axis=0)

        elif self.direction == 2 :
            self.sensor_read.update({'depan' : self.obstacle[self.current[0]-1,self.current[1]]})
            if self.sensor_read['depan'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0]-1,self.current[1]]],axis=0)

            self.sensor_read.update({'belakang' : self.obstacle[self.current[0]+1,self.current[1]]})
            #if self.sensor_read['belakang'] == 2 :
                #self.black_grid = np.append(self.black_grid,[[self.current[0]+1,self.current[1]]],axis=0)

            self.sensor_read.update({'kiri' : self.obstacle[self.current[0],self.current[1]-1]})
            if self.sensor_read['kiri'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0],self.current[1]-1]],axis=0)

            self.sensor_read.update({'kanan' : self.obstacle[self.current[0],self.current[1]+1]})
            if self.sensor_read['kanan'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0],self.current[1]+1]],axis=0)

        elif self.direction == 3 :
            self.sensor_read.update({'depan' : self.obstacle[self.current[0],self.current[1]-1]})
            if self.sensor_read['depan'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0],self.current[1]-1]],axis=0)

            self.sensor_read.update({'belakang' : self.obstacle[self.current[0],self.current[1]+1]})
            #if self.sensor_read['belakang'] == 2 :
                #self.black_grid = np.append(self.black_grid,[[self.current[0],self.current[1]+1]],axis=0)

            self.sensor_read.update({'kiri' : self.obstacle[self.current[0]+1,self.current[1]]})
            if self.sensor_read['kiri'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0]+1,self.current[1]]],axis=0)

            self.sensor_read.update({'kanan' : self.obstacle[self.current[0]-1,self.current[1]]})
            if self.sensor_read['kanan'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0]-1,self.current[1]]],axis=0)

        elif self.direction == 1 :
            self.sensor_read.update({'depan' : self.obstacle[self.current[0],self.current[1]+1]})
            if self.sensor_read['depan'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0],self.current[1]+1]],axis=0)

            self.sensor_read.update({'belakang' : self.obstacle[self.current[0],self.current[1]-1]})
            #if self.sensor_read['belakang'] == 2 :
                #self.black_grid = np.append(self.black_grid,[[self.current[0],self.current[1]-1]],axis=0)

            self.sensor_read.update({'kiri' : self.obstacle[self.current[0]-1,self.current[1]]})
            if self.sensor_read['kiri'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0]-1,self.current[1]]],axis=0)

            self.sensor_read.update({'kanan' : self.obstacle[self.current[0]+1,self.current[1]]})
            if self.sensor_read['kanan'] == 2 :
                self.black_grid = np.append(self.black_grid,[[self.current[0]+1,self.current[1]]],axis=0)

    #fungsi untuk membuat map baru hasil scanning
    def buildmap(self,min,max) :
        if self.created_map.size == 0 :
            self.created_map = np.zeros((max[0]-min[0]+1,max[1]-min[1]+1),dtype=int)
        #black_grid untuk menyimpan koordinat obtacle
        for i in self.black_grid :
            self.created_map[i[0],i[1]] = 1
        #scanning koordinat boundary edges
        for j in self.all_edges :
            if j[0][0]  == j[1][0] and j[0][1]<j[1][1] :
                sisi = np.arange(j[0][1],j[1][1]+1)
                for k in sisi :
                    self.created_map[j[0][0],k] = 3
            elif j[0][0]  == j[1][0] and j[0][1]>j[1][1] :
                sisi = np.arange(j[0][1],j[1][1]-1,-1)
                for k in sisi :
                    self.created_map[j[0][0],k] = 3
            elif j[0][1]  == j[1][1] and j[0][0]<j[1][0] :
                sisi = np.arange(j[0][0],j[1][0]+1)
                for k in sisi :
                    self.created_map[k,j[0][1]] = 3
            elif j[0][1]  == j[1][1] and j[0][0]>j[1][0] :
                sisi = np.arange(j[0][0],j[1][0]-1,-1)
                for k in sisi :
                    self.created_map[k,j[0][1]] = 3

#animasi peta
def forward (i) :
    for i in np.arange(0,i) :
        robot.obstacle[robot.current[0],robot.current[1]] = 0
        robot.moving()
        robot.obstacle[robot.current[0],robot.current[1]] = 1
        im.set_data(robot.obstacle)
        plt.pause(0.01)

#menghitung jarak dua titik pada map
def hitung_jarak(x,y) :
    z = abs(x[1]-y[1]) + abs(x[0]-y[0])
    return z

#deteksi lokasi grid pada edges
def detect_grid_on_what_edges(grid) :
    temp = list()
    for j in robot.all_edges :
        if j[0][0] == j[1][0] and j[0][1]<j[1][1] :
            for ax in range(j[0][1],j[1][1]+1) :
                temp = temp + [[j[0][0],ax]]
        elif j[0][0]  == j[1][0] and j[0][1]>j[1][1] :
            for ax in range(j[1][1],j[0][1]+1) :
                temp = temp + [[j[0][0],ax]]
        elif j[0][1]  == j[1][1] and j[0][0]<j[1][0] :
            for ax in range(j[0][0],j[1][0]+1) :
                temp = temp + [[ax,j[0][1]]]
        elif j[0][1]  == j[1][1] and j[0][0]>j[1][0] :
            for ax in range(j[1][0],j[0][0]+1) :
                temp = temp + [[ax,j[0][1]]]

        if grid in temp :
            return j

    return [[]]

#ekplorasi outer map
def map_exploration () :
    origin = False
    posisi = robot.current.copy()
    convex = list()
    concave = list()
    concave_plus_convex = list()
    obstacle = list()

    while not origin :
        #cek apakah kembali ke titik awal sebelum eksplorasi
        forward(1)
        origin = np.array_equal(robot.current, posisi , equal_nan=False)

        while True :
            robot.sensor()
            if robot.sensor_read['depan'] == 2 : #deteksi concave / tetap jalan
                if robot.sensor_read['kanan'] == 2 and robot.sensor_read['kiri'] == 0 :
                    robot.direction = robot.direction + 1
                    robot.direction = robot.direction % 4
                    concave.append(robot.current.copy())
                    concave_plus_convex.append(robot.current.copy())


                elif robot.sensor_read['kiri'] == 2 and robot.sensor_read['kanan'] == 0 :
                    robot.direction = robot.direction - 1
                    robot.direction = robot.direction % 4
                    concave.append(robot.current.copy())
                    concave_plus_convex.append(robot.current.copy())

                elif robot.sensor_read['kiri'] == 2 and robot.sensor_read['kanan'] == 2 :
                    origin = True
                else :
                    origin = True

            elif robot.sensor_read['depan'] != 2 :  #deteksi convex / tetap jalan
                if robot.sensor_read['kanan'] == 2 and robot.sensor_read['kiri'] == 0 :
                    pass
                elif robot.sensor_read['kiri'] == 2 and robot.sensor_read['kanan'] == 0 :
                    pass
                elif robot.sensor_read['kiri'] == 2 and robot.sensor_read['kanan'] == 2 :
                    origin = True
                elif robot.sensor_read['kiri'] == 0 and robot.sensor_read['kanan'] == 0 :
                    if robot.sensor_read_before['kanan'] == 2 :
                        robot.direction = robot.direction - 1
                        robot.direction = robot.direction % 4
                        convex.append(robot.current.copy())
                        concave_plus_convex.append(robot.current.copy())

                    elif robot.sensor_read_before['kiri'] == 2 :
                        robot.direction = robot.direction + 1
                        robot.direction = robot.direction % 4
                        convex.append(robot.current.copy())
                        concave_plus_convex.append(robot.current.copy())

                    else :
                        origin = True
                else :
                    origin = True

            break

    #memasukkan data nodes convex dan concave ke database
    konversi_convex = np.array(convex)
    konversi_concave = np.array(concave)

    nodes = np.array(concave_plus_convex)

    edges = list()
    for i in range(len(nodes)) :
        if i <= (len(nodes)-2) :
            temp = [nodes[i],nodes[i+1]]
            edges.append(temp.copy())
        else :
            temp = [nodes[i],nodes[0]]
            edges.append(temp.copy())

    konversi_boundaryedges = np.array(edges)

    #menentukan koordinat max dan minimum
    max = np.amax(robot.black_grid, axis=0)
    min = np.amin(robot.black_grid, axis=0)

    robot.buildmap(min,max)

    return(konversi_convex,konversi_concave,konversi_boundaryedges)

#fungsi untuk menambah edges dan nodes
def tambah_edges(all_edges,edges,all_nodes) :
    deleted_edges = np.empty((0,2,2),dtype=int)
    deleted_nodes = np.empty((0,2),dtype=int)
    for z in (0,1) :
        s= 0
        for j in all_edges :
            if j[0][0] == j[1][0] and j[0][1]<j[1][1] :
                sisi = np.arange(j[0][1]+1,j[1][1])
                for k in sisi :
                    v = np.array(edges[z]) == np.array([j[0][0],k])
                    if v.all() :
                        #memisahkan edges yang berpotongan dengan edges baru
                        temp_1 = np.array([j[0],edges[z]])
                        temp_2 = np.array([edges[z],j[1]])
                        #menghapus edges dan nodes lama yang sudah terpotong
                        all_edges = np.delete(all_edges, s,axis=0)
                        deleted_edges = np.append(deleted_edges,[j],axis=0)
                        #memasukkan edges baru
                        all_edges = np.append(all_edges,[temp_1],axis=0)
                        all_edges = np.append(all_edges,[temp_2],axis=0)
                        #memasukkan nodes baru
                        all_nodes = np.append(all_nodes,[edges[z]],axis=0)


            elif j[0][0]  == j[1][0] and j[0][1]>j[1][1] :
                sisi = np.arange(j[0][1]-1,j[1][1],-1)
                for k in sisi :
                    v = np.array(edges[z]) == np.array([j[0][0],k])
                    if v.all() :
                        #memisahkan edges yang berpotongan dengan edges baru
                        temp_1 = np.array([j[0],edges[z]])
                        temp_2 = np.array([edges[z],j[1]])
                        #menghapus edges lama yang sudah terpotong
                        all_edges = np.delete(all_edges, s,axis=0)
                        deleted_edges = np.append(deleted_edges,[j],axis=0)
                        #memasukkan
                        all_edges = np.append(all_edges,[temp_1],axis=0)
                        all_edges = np.append(all_edges,[temp_2],axis=0)
                        #memasukkan nodes baru
                        all_nodes = np.append(all_nodes,[edges[z]],axis=0)


            elif j[0][1]  == j[1][1] and j[0][0]<j[1][0] :
                sisi = np.arange(j[0][0]+1,j[1][0])
                for k in sisi :
                    v = np.array(edges[z]) == np.array([k,j[0][1]])
                    if v.all() :
                        #memisahkan edges yang berpotongan dengan edges baru
                        temp_1 = np.array([j[0],edges[z]])
                        temp_2 = np.array([edges[z],j[1]])
                        #menghapus edges lama yang sudah terpotong
                        all_edges = np.delete(all_edges, s,axis=0)
                        deleted_edges = np.append(deleted_edges,[j],axis=0)
                        #memasukkan
                        all_edges = np.append(all_edges,[temp_1],axis=0)
                        all_edges = np.append(all_edges,[temp_2],axis=0)
                        #memasukkan nodes baru
                        all_nodes = np.append(all_nodes,[edges[z]],axis=0)


            elif j[0][1]  == j[1][1] and j[0][0]>j[1][0] :
                sisi = np.arange(j[0][0]-1,j[1][0],-1)
                for k in sisi :
                    v = np.array(edges[z]) == np.array([k,j[0][1]])
                    if v.all() :
                        #memisahkan edges yang berpotongan dengan edges baru
                        temp_1 = np.array([j[0],edges[z]])
                        temp_2 = np.array([edges[z],j[1]])
                        #menghapus edges lama yang sudah terpotong
                        all_edges = np.delete(all_edges, s,axis=0)
                        deleted_edges = np.append(deleted_edges,[j],axis=0)
                        #memasukkan
                        all_edges = np.append(all_edges,[temp_1],axis=0)
                        all_edges = np.append(all_edges,[temp_2],axis=0)
                        #memasukkan nodes baru
                        all_nodes = np.append(all_nodes,[edges[z]],axis=0)

            s = s+1
            all_edges = np.append(all_edges,[edges],axis = 0)

    return(all_edges,all_nodes,deleted_edges,deleted_nodes)

#menambahkan decomposition edges
def decomposition_edges(konversi_convex) :
    #menentukan decomposition edges dari convex
    konversi_decompositionedges = list()

    for i in konversi_convex :
        ex = list()
        cek = True
        j = 0
        #utara
        while cek :
            j = j + 1
            temp = [i,[i[0]+j,i[1]]]
            if robot.created_map[i[0]+j,i[1]] == 3 :
                cek = False
                if j==1 :
                    pass
                else :
                    ex.append(temp.copy())
            else :
                pass
        #barat
        cek = True
        j = 0
        while cek :
            j = j + 1
            temp = [i,[i[0],i[1]+j]]
            if robot.created_map[i[0],i[1]+j] == 3 :
                cek = False
                if j==1 :
                    pass
                else :
                    ex.append(temp.copy())
            else :
                pass

        #selatan
        cek = True
        j = 0
        while cek :
            j = j + 1
            temp = [i,[i[0]-j,i[1]]]
            if robot.created_map[i[0]-j,i[1]] == 3 :
                cek = False
                if j==1 :
                    pass
                else :
                    ex.append(temp.copy())
            else :
                pass

        #timur
        cek = True
        j = 0
        while cek :
            j = j + 1
            temp = [i,[i[0],i[1]-j]]
            if robot.created_map[i[0],i[1]-j] == 3 :
                cek = False
                if j==1 :
                    pass
                else :
                    ex.append(temp.copy())
            else :
                pass


        n = randint(0,len(ex)-1)
        konversi_decompositionedges.append(ex[n].copy())

    robot.buildmap(min,max)

    return(konversi_decompositionedges)

#algoritma untuk mencari submap
def  djikstra(edges,nodes,start,stop) :

    list_of_submap = list()
    temp_submap = list()
    unvisited_vertex = np.copy(nodes)
    visited_vertex = np.empty((0,2),dtype=int)

    size = nodes.size[0]
    previous_vertex = np.zeros((size,2),dtype=int)

    shortest_from_origin = np.empty((0),dtype=int)
    previous_vertex = np.empty((0,2),dtype=int)

    for ax in nodes :
        v  = ax == start
        if v.all()  :
            shortest_from_origin = np.append(shortest_from_origin,[0])
        else :
            shortest_from_origin = np.append(shortest_from_origin,[99999])

    posisi = start

    while unvisited_vertex.size != 0 :

        for ax in edges :

            v = np.array(posisi) == np.array(ax[0])
            if v.all() :
                if not ax[1] in visited_vertex :
                    temp = shortest_from_origin[np.argwhere(np.all(edges==posisi, axis=1))] + hitung_jarak(posisi,ax[1])
                        if temp < shortest_from_origin[np.argwhere(np.all(edges==ax[1], axis=1))] :
                            shortest_from_origin[np.argwhere(np.all(edges==ax[1], axis=1))] = temp
                            previous_vertex[np.argwhere(np.all(edges==ax[1], axis=1))] = posisi

            v = np.array(posisi) == np.array(ax[1])
            if v.all() :
                if not ax[0] in visited_vertex :
                    temp = shortest_from_origin[np.argwhere(np.all(edges==posisi, axis=1))] + hitung_jarak(posisi,ax[0])
                        if temp < shortest_from_origin[np.argwhere(np.all(edges==ax[0], axis=1))] :
                            shortest_from_origin[np.argwhere(np.all(edges==ax[0], axis=1))] = temp
                            previous_vertex[np.argwhere(np.all(edges==ax[0], axis=1))] = posisi

        visited_vertex = np.append(visited_vertex,[posisi],axis=0)
        unvisited_vertex =  np.delete(unvisited_vertex, np.argwhere(np.all(unvisited_vertex==posisi, axis=1)),0)

        i=0
        posisi = unvisited_vertex[i]
        temp = shortest_from_origin[np.argwhere(np.all(edges==posisi, axis=1))]

        for i in range(1,unvisited_vertex.size[0]) :
            if shortest_from_origin[np.argwhere(np.all(edges==unvisited_vertex[i], axis=1))] < temp :
                posisi = unvisited_vertex[i]
                temp = shortest_from_origin[np.argwhere(np.all(edges==unvisited_vertex[i], axis=1))]
            i = i+1

    temp = stop
    v = temp != start
    while v.all()  :
        temp_submap = [previous_vertex[np.argwhere(np.all(edges==temp, axis=1))]]
        list_of_submap = list_of_submap + temp_submap

        temp = previous_vertex[np.argwhere(np.all(edges==temp, axis=1))]
        v = temp != start

    return list_of_submap

#fungsi untuk menghapus edges dan nodes
def hapus_edges(all_edges,all_nodes,intersect_nodes,intersect_edges) :
    deleted_edges =  np.empty((0,2,2),dtype=int)
    deleted_nodes  =  np.empty((0,2),dtype=int)

    for ax in intersect_edges :
        if ax in all_edges :
            all_edges = np.delete(all_edges, np.argwhere(np.all(all_edges==ax, axis=(1, 2))),0)

    deleted_edges = np.copy(intersect_edges)
    deleted_nodes = np.copy(intersect_nodes)

    return(all_edges,all_nodes,deleted_edges,deleted_nodes)


#membuat edges dari nodes-nodes yang berurutan
def create_submap_from_nodes_to_edges (nodes) :
    temp_edges = list()
    final_edges = list()
    for i in range(0,len(nodes)) :
        if i != len(nodes)-1 :
            temp_edges = [nodes[i],nodes[i+1]]
            final_edges = final_edges + [temp_edges]
        else :
            temp_edges = [nodes[-1],nodes[0]]
            final_edges = final_edges + [temp_edges]

    return final_edges

def move_from_to (source_grid,destination_grid) :
    if source_grid[0]<destination_grid[0] :
        robot.direction = 1
        forward(destination_grid-source_grid)
    elif source_grid[0]>destination_grid[0] :
        robot.direction = 3
        forward(source_grid-destination_grid)
    else :
        pass

    if source_grid[1]<destination_grid[1] :
        robot.direction = 0
        forward(destination_grid-source_grid)
    elif source_grid[1]>destination_grid[1] :
        robot.direction = 2
        forward(destination_grid-source_grid)
    else :
        pass


#membersihkan submap yang dipilih dengan metode spiral
def cleaning(submap,cleaned_submap) :
    jalur_membersihkan = list()
    jalur_pindah_submap = list()
    done = False

    while not done :

        if len(submap) != 0 :
            starting_point = submap[0][0]
            for ax in submap :
                for bx in ax :
                    temp_1 = hitung_jarak(robot.current, starting_point)
                    temp_2  = hitung_jrak(robot.current,bx)
                    if temp_2 < temp_1  :
                        starting_point  = bx


#identifikasi submap yang harus digabungkan saat terdeteksi obstacle
def map_exploration_obstacle_detected() :
    submap_to_merge = list()

    origin = False
    posisi = robot.current.copy()
    convex = list()
    concave = list()
    obstacle = list()

    temp = list()
    intersect_edges = np.empty((0,2,2),dtype=int)
    intersect_nodes = np.empty((0,2),dtype=int)
    deleted_submap = list()
    all_edges = np.empty((0,2,2),dtype=int)

    while not origin :
        #cek apakah kembali ke titik awal sebelum eksplorasi
        forward(1)
        origin = np.array_equal(robot.current, posisi , equal_nan=False)

        while True :
            robot.sensor()
            if robot.sensor_read['depan'] == 2 : #deteksi concave / tetap jalan
                if robot.sensor_read['kanan'] == 2 and robot.sensor_read['kiri'] == 0 :
                    robot.direction = robot.direction + 1
                    robot.direction = robot.direction % 4
                    concave.append(robot.current.copy())
                    concave_plus_convex.append(robot.current.copy())


                elif robot.sensor_read['kiri'] == 2 and robot.sensor_read['kanan'] == 0 :
                    robot.direction = robot.direction - 1
                    robot.direction = robot.direction % 4
                    concave.append(robot.current.copy())
                    concave_plus_convex.append(robot.current.copy())

                elif robot.sensor_read['kiri'] == 2 and robot.sensor_read['kanan'] == 2 :
                    origin = True
                else :
                    origin = True

            elif robot.sensor_read['depan'] != 2 :  #deteksi convex / tetap jalan
                if robot.sensor_read['kanan'] == 2 and robot.sensor_read['kiri'] == 0 :
                    pass
                elif robot.sensor_read['kiri'] == 2 and robot.sensor_read['kanan'] == 0 :
                    pass
                elif robot.sensor_read['kiri'] == 2 and robot.sensor_read['kanan'] == 2 :
                    origin = True
                elif robot.sensor_read['kiri'] == 0 and robot.sensor_read['kanan'] == 0 :
                    if robot.sensor_read_before['kanan'] == 2 :
                        robot.direction = robot.direction - 1
                        robot.direction = robot.direction % 4
                        convex.append(robot.current.copy())
                        concave_plus_convex.append(robot.current.copy())

                    elif robot.sensor_read_before['kiri'] == 2 :
                        robot.direction = robot.direction + 1
                        robot.direction = robot.direction % 4
                        convex.append(robot.current.copy())
                        concave_plus_convex.append(robot.current.copy())

                    else :
                        origin = True
                else :
                    origin = True

            #memasukkan data edges dan nodes yang bersinggungan
            if robot.created_map[robot.current[0],robot.current[1]] == 2 :
                temp = detect_grid_on_what_edges(robot.current)
                if not temp in intersect_edges :
                    intersect_edges = np.append(intersect_edges,[temp],axis = 0)
                    intersect_nodes = np.append(intersect_nodes,[temp[0]],axis = 0)
                    intersect_nodes = np.append(intersect_nodes,[temp[1]],axis = 0)

            break

    #deteksi submap yang di merge dan submap yang dihapus
    for cx in submap :
        if intersect_edges[0] in cx and intersect_edges[1] in cx :
            if not cx in deleted_submap :
                deleted_submap.append(cx.copy())

    #identifikasi edges dan nodes pada submap yang di merge
    for dx in deleted_submap :
        temp = create_submap_from_nodes_to_edges(dx)
        for ex in dx :
            if not ex in all_nodes :
                all_nodes = np.append(all_nodes,[ex],axis=0)

        for fx in temp :
            if not fx in all_edges:
                all_edges = np.append(all_edges,[fx],axis=0)


    #memasukkan data nodes convex dan concave ke database
    konversi_convex = np.array(convex)
    konversi_concave = np.array(concave)

    nodes = np.array(concave_plus_convex)

    edges = list()
    for i in range(len(nodes)) :
        if i <= (len(nodes)-2) :
            temp = [nodes[i],nodes[i+1]]
            edges.append(temp.copy())
        else :
            temp = [nodes[i],nodes[0]]
            edges.append(temp.copy())

    konversi_boundaryedges = np.array(edges)

    #menentukan koordinat max dan minimum
    max = np.amax(robot.black_grid, axis=0)
    min = np.amin(robot.black_grid, axis=0)

    robot.buildmap(min,max)

    return(konversi_convex,konversi_concave,konversi_boundaryedges,deleted_submap,all_edges,all_nodes,intersect_edges,intersect_nodes)


def init () :
    robot.obstacle[robot.current[0],robot.current[1]] = 1
    im.set_data(robot.obstacle)
    plt.pause(0.01)

def main() :
    init()

    concave = np.empty((0,2),dtype=int)
    convex = np.empty((0,2),dtype=int)
    boundary_edges = np.empty((0,2,2),dtype=int)
    decomposition_edges = np.empty((0,2,2),dtype=int)
    all_edges = np.empty((0,2,2),dtype=int)
    all_nodes = np.empty((0,2),dtype=int)

    done = False

    #menyimpan nodes  yang bersinggungan sebelum merge submap dilakukan
    intersect_nodes = np.empty((0,2),dtype=int)
    intersect_edges = np.empty((0,2,2),dtype=int)

    #tempat menyimpan nodes dan edges submap yang akan di merge
    outer_nodes =  np.empty((0,2),dtype=int)
    outer_edges = np.empty((0,2,2),dtype=int)

    #menyimpan submap yang belum di bersihkan dan yang belum dibersihkan
    uncleaned_submap = list()
    cleaned_submap = list()

    #mencari  concave, convex, dan boundary edges untuk obstacle
    convex,concave,boundary_edges = map_exploration()

    #outer edges dimasukkan ke semua edges
    all_edges = np.append(all_edges,outer_edges,axis=0)

    #menghapus edges yang intersect
    deleted_edges,deleted_nodes = hapus_edges(all_edges,intersect_nodes,intersect_edges)

    #mengisi decomposistion edges
    decomposition_edges = decomposition_edges(convex)

    #tambahkan decomposition edges ke all edges
    all_edges =  np.append(all_edges,decomposition_edges,axis=0)

    #tambah decomposition edges untuk diintegrasi dengan semua edges
    for bx in decomposition_edges :
        all_edges,all_nodes = tambah_edges(all_edges,bx,all_nodes)

    #mencari submap menggunakan algoritma djikstra
    uncleaned_submap = djikstra(all_edges,all_nodes)

    while not done :
    #membersihkan submap
        cleaned_submap,uncleaned_submap,done = cleaning()





    plt.show()



#tampilan peta
fig = plt.figure()
ax = plt.axes()
im = ax.imshow(robot.obstacle,cmap=cmap)
ax.set_xticks(np.arange(0,16,1))
ax.set_yticks(np.arange(0,16,1))
ax.set_xticklabels(np.arange(0, 16, 1))
ax.set_yticklabels(np.arange(0, 16, 1))
ax.set_xticks(np.arange(-.5, 16.5,1), minor = True)
ax.xaxis.tick_top()
ax.set_yticks(np.arange(-.5, 16.5,1), minor = True)
ax.grid(which='minor', axis = 'both',color='grey', linestyle='-', linewidth=1)

main()
