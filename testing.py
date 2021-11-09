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

    #alarm deteksi objek terdekat
    def object_alert_nearby(self)
        if self.sensor_read['depan']==2 or self.sensor_read['kiri']==2 or self.sensor_read['kanan'] == 2 :
            return True
        else :
            return False

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

#membuat list grid dari dua nodes
def create_list_of_grid_from_two_nodes (source_nodes,destination_nodes) :
    output = np.empty((0,2),dtype=int)
    if source_nodes[0] == destination_nodes[0] and source_nodes[1]<destination_nodes[1] :
        for i in range(source_nodes[1],destination_nodes[1]+1) :
            output = np.append(output,[source_nodes[0],i],axis=0)
    elif source_nodes[0] == destination_nodes[0] and source_nodes[1]>destination_nodes[1] :
        for i in range(source_nodes[1],destination_nodes[1]-1,-1) :
            output = np.append(output,[source_nodes[0],i],axis=0)
    elif source_nodes[1] == destination_nodes[1] and source_nodes[0]<destination_nodes[0] :
        for i in range(source_nodes[0],destination_nodes[0]+1) :
            output = np.append(output,[source_nodes[1],i],axis=0)
    elif source_nodes[1] == destination_nodes[1] and source_nodes[0]>destination_nodes[0] :
        for i in range(source_nodes[0],destination_nodes[0]-1,-1) :
            output = np.append(output,[source_nodes[1],i],axis=0)
    else :
        pass

    return output

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
    convex = np.array(convex)
    concave = np.array(concave)

    nodes = np.array(concave_plus_convex)

    edges = list()
    for i in range(len(nodes)) :
        if i <= (len(nodes)-2) :
            temp = [nodes[i],nodes[i+1]]
            edges.append(temp.copy())
        else :
            temp = [nodes[i],nodes[0]]
            edges.append(temp.copy())

    edges = np.array(edges)

    deleted_edges = np.empty((0,2,2),dtype=int)
    deleted_nodes = np.empty((0,2),dtype=int)
    submap = []
    #perbaharui edges,nodes, dan submap map
    update_map_component(nodes,edges,submap,deleted_nodes,deleted_edges,deleted_submap)

    #menentukan koordinat max dan minimum
    max = np.amax(robot.black_grid, axis=0)
    min = np.amin(robot.black_grid, axis=0)

    robot.buildmap(min,max)

    return(convex)

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


    #perbaharui edges,nodes, dan submap map
    update_map_component(all_nodes,all_edges,submap,deleted_nodes,deleted_edges,deleted_submap)

    #menentukan koordinat max dan minimum
    max = np.amax(robot.black_grid, axis=0)
    min = np.amin(robot.black_grid, axis=0)

    robot.buildmap(min,max)

#menambahkan decomposition edges
def decomposition_edges(convex) :
    #menentukan decomposition edges dari convex
    decompositionedges = list()

    for i in convex :
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
        decomposition_edges.append(ex[n].copy())


    return(decomposition_edges)

#algoritma untuk mencari submap
def djikstra(all_edges,all_nodes,start,stop) :

    submap = list()
    temp_submap = list()
    unvisited_vertex = np.copy(all_nodes)
    visited_vertex = np.empty((0,2),dtype=int)

    size = all_nodes.size[0]
    previous_vertex = np.zeros((size,2),dtype=int)

    shortest_from_origin = np.empty((0),dtype=int)
    previous_vertex = np.empty((0,2),dtype=int)

    for ax in all_nodes :
        v  = ax == start
        if v.all()  :
            shortest_from_origin = np.append(shortest_from_origin,[0])
        else :
            shortest_from_origin = np.append(shortest_from_origin,[99999])

    posisi = start

    while unvisited_vertex.size != 0 :

        for ax in all_edges :
            #mencari edges yang bisa dilalui dengan cost paling sedikit
            v = np.array(posisi) == np.array(ax[0])
            if v.all() :
                if not ax[1] in visited_vertex :
                    temp = shortest_from_origin[np.argwhere(np.all(all_nodes==posisi, axis=1))] + hitung_jarak(posisi,ax[1])
                        if temp < shortest_from_origin[np.argwhere(np.all(all_nodes==ax[1], axis=1))] :
                            shortest_from_origin[np.argwhere(np.all(all_nodes==ax[1], axis=1))] = temp
                            previous_vertex[np.argwhere(np.all(all_nodes==ax[1], axis=1))] = posisi

            v = np.array(posisi) == np.array(ax[1])
            if v.all() :
                if not ax[0] in visited_vertex :
                    temp = shortest_from_origin[np.argwhere(np.all(all_nodes==posisi, axis=1))] + hitung_jarak(posisi,ax[0])
                        if temp < shortest_from_origin[np.argwhere(np.all(all_nodes==ax[0], axis=1))] :
                            shortest_from_origin[np.argwhere(np.all(all_nodes==ax[0], axis=1))] = temp
                            previous_vertex[np.argwhere(np.all(all_nodes==ax[0], axis=1))] = posisi

        visited_vertex = np.append(visited_vertex,[posisi],axis=0)
        unvisited_vertex =  np.delete(unvisited_vertex, np.argwhere(np.all(unvisited_vertex==posisi, axis=1)),0)

        #mencari next unvisited vertex dengan cost terkecil
        i=0
        posisi = unvisited_vertex[i]
        temp = shortest_from_origin[np.argwhere(np.all(all_nodes==posisi, axis=1))]

        for i in range(1,unvisited_vertex.size[0]) :
            if shortest_from_origin[np.argwhere(np.all(all_nodes==unvisited_vertex[i], axis=1))] < temp :
                posisi = unvisited_vertex[i]
                temp = shortest_from_origin[np.argwhere(np.all(all_nodes==unvisited_vertex[i], axis=1))]
            i = i+1

    #membuat jalur tercepat dari titik start ke stop
    temp = stop
    v = temp != start
    while v.all()  :
        temp_submap = [previous_vertex[np.argwhere(np.all(all_nodes==temp, axis=1))]]
        submap = submap + temp_submap

        temp = previous_vertex[np.argwhere(np.all(all_nodes==temp, axis=1))]
        v = temp != start

    return submap

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

#fungsi bergerak dari satu grid ke grid lainnya
def move_from_to (source_grid,destination_grid) :
    if source_grid[0]<destination_grid[0] :
        robot.direction = 1
        for  i in range(0,destination_grid-source_grid-1) :
            obstacle_detected  = robot.object_alert_nearby()
            if not  obstacle_detected  :
                forward(1)
            else
                return True

    elif source_grid[0]>destination_grid[0] :
        robot.direction = 3
        for  i in range(0,source_grid-destination_grid-1) :
            obstacle_detected  = robot.object_alert_nearby()
            if not  obstacle_detected  :
                forward(1)
            else
                return True
    else
        pass

    if source_grid[1]<destination_grid[1] :
        robot.direction = 0
        for  i in range(0,destination_grid-source_grid-1) :
            obstacle_detected  = robot.object_alert_nearby()
            if not  obstacle_detected  :
                forward(1)
            else
                return True

    elif source_grid[1]>destination_grid[1] :
        robot.direction = 2
        for  i in range(0,source_grid-destination_grid-1) :
            obstacle_detected  = robot.object_alert_nearby()
            if not  obstacle_detected  :
                forward(1)
            else
                return True
    else
        pass

    return False

def sign(value) :
    if value > 0 :
        return 1
    elif value < 0 :
        return -1
    else :
        return 0

#mencari neighbor grid untuk cleaning submap
def neighbor_grid_inside_submap(previous_submap) :
    max_grid = max(previous_submap)
    min_grid = min(previous_submap)

    for ax in previous_submap :
        neighbor_grid = [[ax[0]+1,ax[1]],[ax[0],ax[1]+1],[ax[0]-1,ax[1]],[ax[0],ax[1]-1],[ax[0]+1,ax[1]+1],[ax[0]-1,ax[1]-1],[ax[0]+1,ax[1]-1],[ax[0]-1,ax[1]+1]]
        for bx in neighbor_grid :
            T = sign(bx[0]-max_grid[0]) + sign(bx[1]-max_grid[1]) + sign(bx[0]-min_grid[0]) + sign(bx[1]-min_grid[1])

            if T == 0 :
                next_submap =

#membersihkan submap yang dipilih dengan metode spiral
def cleaning(submap) :
    jalur_membersihkan = list()
    done = False
    obstacle_detected = False

    while not done :
        pass

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

    #eksplorasi map utama
    convex = map_exploration()
    #mencari decomposisiton edges
    decomposition_edeges = decomposition_edeges(convex)
    #menambahkan decomposition edges ke komponen map
    for ax in decomposition_edeges :
        tambah_edges(robot.all_edges,ax,robot.all_nodes)

    #mencari submap
    all_edges = np.copy(robot.all_edges)
    all_nodes = np.copy(robot.all_nodes)
    submap = list()
    all_subamps = list()
    deleted_edges_in_process_to_find_submap = list()

    for bx in all_edges :
        if bx in all_edges :
            all_edges = np.delete(all_edges, np.argwhere(np.all(all_edges==bx, axis=(1, 2))),0)
            submap = djikstra(all_edges,all_nodes,bx[0],bx[1])
            all_submaps.append(submap)
            all_edges = np.append(all_edges,[bx],axis= 0)
            deleted_edges_in_process_to_find_submap = create_submap_from_nodes_to_edges(submap)
            for cx in deleted_edges_in_process_to_find_submap :
                all_edges = np.delete(all_edges, np.argwhere(np.all(all_edges==cx, axis=(1, 2))),0)

    all_edges = np.empty((0,2,2),dtype=int)
    all_nodes = np.empty((0,2),dtype=int)
    deleted_nodes = np.empty((0,2),dtype=int)
    deleted_edges = np.empty((0,2,2),dtype=int)
    submap = all_submaps
    deleted_submap = list()

    #perbaharui edges,nodes, dan submap map
    update_map_component(all_nodes,edges,submap,deleted_nodes,deleted_edges,deleted_submap)


    #proses pembersihan
    submaps = np.copy(robot.submap)
    all_edges = np.copy(robot.all_edges)
    all_nodes = np.copy(robot.all_nodes)

    for ax in submaps :
        #cek jumlah convex dan concave corner
        for bx in ax :
            index = ax.index(bx)
            if index == 0 :
                neighbor_nodes = [ax[-1],ax[ax[index+1]]]
            elif index == len(ax)-1 :
                neighbor_nodes = [ax[index-1],ax[0]]
            else :
                neighbor_nodes = [ax[index+1],ax[ax[index-1]]]

            #cek neighbor grid pada edges yang terhubung ke nodes bersangkutan
            neighbor_grid = [[bx[0]+1,bx[1]],[bx[0],bx[1]+1],[bx[0]-1,bx[1]],[bx[0],bx[1]-1]]
            for cx in neighbor_nodes :
                list_of_grid_between_focusednodes_and_neighbornodes = create_list_of_grid_from_two_nodes(bx,cx)

            #pemilihan noughbor grid yang cocok untuk menentukan tipe nodes/corner
            chosen_neighbor_grid = np.empty((0,2),dtype=int)
            for dx in neighbor_grid :
                if dx in list_of_grid_between_focusednodes_and_neighbornodes :
                    chosen_neighbor_grid = np.append(chosen_neighbor_grid,[dx],axis=0)

            temp = list()
            for ex in chosen_neighbor_grid :
                temp = temp + [[ex[0]+1,ex[1]],[ex[0],ex[1]+1],[ex[0]-1,ex[1]],[ex[0],ex[1]-1]]

            #cek grid yang sama pada chosen_neighbor_grid
            for fx in temp :




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
