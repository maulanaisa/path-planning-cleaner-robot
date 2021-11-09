import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from random import randint
import math

#map colour : white (open space), blue (robot), black (outer boundary)
cmap = colors.ListedColormap(['white','blue','black'])

#map information : matriks, boudary submap, boundary obstacle, arah, posisi robot, all_nodes

class peta :
    #current[row,column]
    current = np.array ([1,1])
    # 0 = utara, 1 = barat, 2 = selatan, 3 = timur
    direction = 0
    sensor_read = {'depan' : 0, 'belakang' : 0, 'kanan' : 0, 'kiri' : 0}
    sensor_read_before = {'depan' : 0, 'belakang' : 0, 'kanan' : 0, 'kiri' : 0}

    boundary_edges = np.empty((0,2,2),dtype=int)
    decomposition_edges = np.empty((0,2,2),dtype=int)
    all_edges = np.empty((0,2,2),dtype = int)
    convex = np.empty((0,2),dtype=int)
    concave = np.empty((0,2),dtype=int)
    intersection = np.empty((0,2),dtype=int)
    all_nodes = np.empty((0,2),dtype = int)
    black_grid = np.empty((0,2),dtype=int)
    submap = np.empty((0,4,2),dtype=int)

    created_map = np.empty((0,0),dtype=int)

    obstacle = np.array ([
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,2,2,2,0,0,2],
        [2,0,0,0,0,0,0,0,0,0,2,2,2,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,2,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,2,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,2,0,0,0,0,2],
        [2,2,2,2,2,2,0,0,0,0,2,0,0,0,0,2],
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



    #fungsi untuk menambah edges
    def tambah_edges(self,edges) :
        for z in (0,1) :
            s= 0
            for j in self.all_edges :
                if j[0][0] == j[1][0] and j[0][1]<j[1][1] :
                    sisi = np.arange(j[0][1]+1,j[1][1])
                    for k in sisi :
                        v = np.array(edges[z]) == np.array([j[0][0],k])
                        if v.all() :
                            #memisahkan edges yang berpotongan dengan edges baru
                            temp_1 = np.array([j[0],edges[z]])
                            temp_2 = np.array([edges[z],j[1]])
                            #menghapus edges dan nodes lama yang sudah terpotong
                            self.all_edges = np.delete(self.all_edges, s,axis=0)
                            #memasukkan edges baru
                            self.all_edges = np.append(self.all_edges,[temp_1],axis=0)
                            self.all_edges = np.append(self.all_edges,[temp_2],axis=0)
                            #memasukkan nodes baru
                            self.all_nodes = np.append(self.all_nodes,[edges[z]],axis=0)
                            self.intersection = np.append(self.intersection,[edges[z]],axis=0)


                elif j[0][0]  == j[1][0] and j[0][1]>j[1][1] :
                    sisi = np.arange(j[0][1]-1,j[1][1],-1)
                    for k in sisi :
                        v = np.array(edges[z]) == np.array([j[0][0],k])
                        if v.all() :
                            #memisahkan edges yang berpotongan dengan edges baru
                            temp_1 = np.array([j[0],edges[z]])
                            temp_2 = np.array([edges[z],j[1]])
                            #menghapus edges lama yang sudah terpotong
                            self.all_edges = np.delete(self.all_edges, s,axis=0)
                            #memasukkan
                            self.all_edges = np.append(self.all_edges,[temp_1],axis=0)
                            self.all_edges = np.append(self.all_edges,[temp_2],axis=0)
                            #memasukkan nodes baru
                            self.all_nodes = np.append(self.all_nodes,[edges[z]],axis=0)
                            self.intersection = np.append(self.intersection,[edges[z]],axis=0)


                elif j[0][1]  == j[1][1] and j[0][0]<j[1][0] :
                    sisi = np.arange(j[0][0]+1,j[1][0])
                    for k in sisi :
                        v = np.array(edges[z]) == np.array([k,j[0][1]])
                        if v.all() :
                            #memisahkan edges yang berpotongan dengan edges baru
                            temp_1 = np.array([j[0],edges[z]])
                            temp_2 = np.array([edges[z],j[1]])
                            #menghapus edges lama yang sudah terpotong
                            self.all_edges = np.delete(self.all_edges, s,axis=0)
                            #memasukkan
                            self.all_edges = np.append(self.all_edges,[temp_1],axis=0)
                            self.all_edges = np.append(self.all_edges,[temp_2],axis=0)
                            #memasukkan nodes baru
                            self.all_nodes = np.append(self.all_nodes,[edges[z]],axis=0)
                            self.intersection = np.append(self.intersection,[edges[z]],axis=0)


                elif j[0][1]  == j[1][1] and j[0][0]>j[1][0] :
                    sisi = np.arange(j[0][0]-1,j[1][0],-1)
                    for k in sisi :
                        v = np.array(edges[z]) == np.array([k,j[0][1]])
                        if v.all() :
                            #memisahkan edges yang berpotongan dengan edges baru
                            temp_1 = np.array([j[0],edges[z]])
                            temp_2 = np.array([edges[z],j[1]])
                            #menghapus edges lama yang sudah terpotong
                            self.all_edges = np.delete(self.all_edges, s,axis=0)
                            #memasukkan
                            self.all_edges = np.append(self.all_edges,[temp_1],axis=0)
                            self.all_edges = np.append(self.all_edges,[temp_2],axis=0)
                            #memasukkan nodes baru
                            self.all_nodes = np.append(self.all_nodes,[edges[z]],axis=0)
                            self.intersection = np.append(self.intersection,[edges[z]],axis=0)

                s = s+1
        self.decomposition_edges = np.append(self.decomposition_edges,[edges],axis=0)
        self.all_edges = np.append(self.all_edges,[edges],axis = 0)


    def hapus_edges(self,edges) :
        self.all_edges = np.delete(self.all_edges, np.where(self.all_edges == edges))
        for k in (0,1) :
            for j in self.all_edges :
                if edges[k] in j :
                    #menyimpan sementara edges yang akan digabungkan
                    if j[0] == edges[k] :
                        temp = j[1]
                    else :
                        temp_1 = j[0]
                    #menghapus nodes lama yang sudah terpotong
                    if edges[k] in robot.all_nodes and edges[k] in robot.intersection :
                        self.all_nodes = np.delete(self.all_nodes, np.where(self.all_edges == edges[0]))

            new_edges = [j[0],j[1]]

    def astar(self) :
        #menyimpan edges yang masih bisa dipilih untuk menentukan submap
        temp_hapus = np.copy(self.all_edges)
        #menyimpan edges yang bisa dilewati di tiap point posisi
        temp_jalur = np.copy(self.all_edges)

        for ax in self.all_edges :
            if ax in temp_hapus  :
                #menyimpan jalur pembentuk sub map_exploration
                jalur_submap = np.empty((0,2,2),dtype=int)

                azz = np.where(np.all(temp_jalur==ax, axis=(1, 2)))[0][0]
                temp_jalur = np.delete(temp_jalur, np.argwhere(np.all(temp_jalur==ax, axis=(1, 2))),0)

                temp_hapus = np.delete(temp_hapus, np.argwhere(np.all(temp_hapus==ax, axis=(1, 2))),0)
                save_temp_jalur = np.copy(temp_jalur)

                #menyimpan jalur yang awal sebelum deteksi next submap, misal terjadi kesalahan pembentukan submap
                save_temp_hapus  = np.copy(temp_hapus)

                f = np.empty((0),dtype=int)
                g = np.empty((0),dtype=int)
                h = np.empty((0),dtype=int)

                #menyimpan nodes yang mengelilingi submap sementara di tiap pencarian titik selanjutnya
                submap_nodes = np.empty((0,2),dtype=int)

                #menyimpan edges dari temp_hapus yang kira-kira akan dipilih sebagai jalur
                pre_deleted_edges = np.empty((0,2,2),dtype=int)

                #menyimpan edges submap yang terjadi
                path_choosen =  np.empty((0,2,2),dtype=int)
                path_choosen = np.append(path_choosen,[ax],axis  =0)

                awal = ax[0]
                akhir = ax[1]
                posisi = awal

                #menyimpan final nodes tiap menemukan submap
                final_submap = np.empty((0,2),dtype=int)
                final_submap = np.append(final_submap,[awal],axis=0)

                w = np.array(posisi) == np.array(akhir)
                while not w.all() :

                    for edges in temp_jalur :

                        v = np.array(posisi) == np.array(edges[0])
                        if v.all() :
                            submap_nodes = np.append(submap_nodes,[edges[1]],axis=0)
                            g = np.append(g,[hitung_jarak(posisi,edges[1])])
                            h = np.append(h,[hitung_jarak(edges[1],akhir)])
                            pre_deleted_edges = np.append(pre_deleted_edges,[edges],axis=0)


                        v = np.array(posisi) == np.array(edges[1])
                        if v.all() :
                            submap_nodes = np.append(submap_nodes,[edges[0]],axis=0)
                            g = np.append(g,[hitung_jarak(posisi,edges[0])])
                            h = np.append(h,[hitung_jarak(edges[0],akhir)])
                            pre_deleted_edges = np.append(pre_deleted_edges,[edges],axis=0)

                    f = np.add(g,h)

                    #jika  tidak ada jalan
                    if f.size  == 0 :
                        posisi = awal

                        temp_jalur = np.copy(save_temp_jalur)
                        temp_jalur = np.delete(temp_jalur, np.argwhere(np.all(temp_jalur==last_edges_visited, axis=(1, 2))),0)
                        save_temp_jalur  = np.copy(temp_jalur)

                        temp_hapus = np.copy(save_temp_hapus)

                        final_submap = np.empty((0,2),dtype=int)
                        final_submap = np.append(final_submap,[awal],axis=0)

                        path_choosen =  np.empty((0,2,2),dtype=int)
                        path_choosen = np.append(path_choosen,[ax],axis  =0)

                    else :
                        minimum_submap_nodes = submap_nodes[np.argmin(f)]
                        posisi = submap_nodes[np.argmin(f)]
                        last_edges_visited = pre_deleted_edges[np.argmin(f)]


                        #jika node pilihan kembali ke node awal
                        w  = np.array(posisi) == np.array(awal)
                        if  w.all() :

                            posisi = awal

                            temp_jalur = np.copy(save_temp_jalur)
                            temp_jalur = np.delete(temp_jalur, np.argwhere(np.all(temp_jalur==last_edges_visited, axis=(1, 2))),0)
                            save_temp_jalur  = np.copy(temp_jalur)

                            temp_hapus = np.copy(save_temp_hapus)

                            final_submap = np.empty((0,2),dtype=int)
                            final_submap = np.append(final_submap,[awal],axis=0)

                            path_choosen =  np.empty((0,2,2),dtype=int)
                            path_choosen = np.append(path_choosen,[ax],axis  =0)


                        else :
                            path_choosen =  np.append(path_choosen,[pre_deleted_edges[np.argmin(f)]],axis=0)

                            final_submap = np.append(final_submap,[minimum_submap_nodes],axis=0)

                            temp_hapus = np.delete(temp_hapus, np.argwhere(np.all(temp_hapus==pre_deleted_edges[np.argmin(f)], axis=(1, 2))),0)

                            temp_jalur = np.delete(temp_jalur, np.argwhere(np.all(temp_jalur==pre_deleted_edges[np.argmin(f)], axis=(1, 2))),0)


                    #Reset semua value sebelum mencari submap  selanjutnya
                    f = np.empty((0),dtype=int)
                    g = np.empty((0),dtype=int)
                    h = np.empty((0),dtype=int)
                    pre_deleted_edges = np.empty((0,2,2),dtype=int)
                    submap_nodes = np.empty((0,2),dtype=int)

                    w = np.array(posisi) == np.array(akhir)

                #temp_jalur = np.insert(temp_jalur,azz,[ax],0)
                temp_jalur = np.copy(self.all_edges)

                print(final_submap)
                print()

    def djikstra(self) :
        available_vertex = np.copy(self.all_nodes)
        visited_vertex = np.empty((0,2),dtype=int)
        weight_from_source = np.empty((0),dtype=int)
        path_finder =  np.empty((0,0,2),dtype=int)


        temp_jalur = np.copy(self.all_edges)
        temp_hapus = np.copy(self.all_edges)

        for ax in temp_hapus :
            if ax in temp_hapus :
                start = ax[0]
                finish = ax[1]
                posisi = start

                temp_jalur = np.delete(temp_jalur, np.argwhere(np.all(temp_jalur==ax, axis=(1, 2))),0)
                temp_hapus = np.delete(temp_hapus, np.argwhere(np.all(temp_jalur==ax, axis=(1, 2))),0)

                for bx in available_vertex :
                    if not np.all(bx==posisi) :
                        weight_from_source = np.append(weight_from_source,[inf],axis=0)
                        path_finder = np.append(path_finder,[[0,0]],axis=0)
                    else :
                        weight_from_source = np.append(weight_from_source,[0],axis=0)
                        path_finder = np.append(path_finder,[[posisi]],axis=0)

                while available_vertex.size != 0 :
                    i = 0

                    for edges in temp_jalur :

                        v = np.array(posisi) == np.array(edges[0])
                        if v.all() :
                            list_next_nodes = np.append(list_next_nodes,[edges[1]],axis=0)
                            g = np.append(g,[hitung_jarak(posisi,edges[1])])

                        v = np.array(posisi) == np.array(edges[1])
                        if v.all() :
                            list_next_nodes = np.append(list_next_nodes,[edges[0]],axis=0)
                            g = np.append(g,[hitung_jarak(posisi,edges[0])])

                    for an in list_next_nodes :
                        weight_from_source[np.argwhere(np.all(available_vertex==an, axis=1))[0][0]] = g[0]
                        i=i+1














robot = peta()


def cleaning() :
    pass



def init () :
    robot.obstacle[robot.current[0],robot.current[1]] = 1
    im.set_data(robot.obstacle)
    plt.pause(0.01)


#animasi peta
def forward (i) :
    for i in np.arange(0,i) :
        robot.obstacle[robot.current[0],robot.current[1]] = 0
        robot.moving()
        robot.obstacle[robot.current[0],robot.current[1]] = 1
        im.set_data(robot.obstacle)
        plt.pause(0.01)

def hitung_jarak(x,y) :
    z = abs(x[1]-y[1]) + abs(x[0]-y[0])
    return z


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
    robot.convex = np.append(robot.convex,konversi_convex,axis=0)
    robot.concave = np.append(robot.concave,konversi_concave,axis=0)



    nodes = np.array(concave_plus_convex)
    robot.all_nodes = np.append(robot.all_nodes,nodes,axis=0)

    edges = list()
    for i in range(len(nodes)) :
        if i <= (len(nodes)-2) :
            temp = [nodes[i],nodes[i+1]]
            edges.append(temp.copy())
        else :
            temp = [nodes[i],nodes[0]]
            edges.append(temp.copy())
    konversi_boundaryedges = np.array(edges)

    #tambah boundary edges
    robot.boundary_edges = np.append(robot.boundary_edges,konversi_boundaryedges,axis=0)
    robot.all_edges = np.append(robot.all_edges,konversi_boundaryedges,axis = 0)

    #menentukan koordinat max dan minimum
    max = np.amax(robot.black_grid, axis=0)
    min = np.amin(robot.black_grid, axis=0)

    robot.buildmap(min,max)

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

    #tambah decomposition edges
    for bx in konversi_decompositionedges :
        robot.tambah_edges(bx)

    robot.buildmap(min,max)

    print(robot.created_map)

def main() :
    init()

    map_exploration()
    robot.astar()
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
