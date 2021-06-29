class Car:
    def __init__(self, x, y):
        self.pt = myPoint(x, y)
        self.x = x
        self.y = y
        self.width = 14
        self.height = 30

        self.points = 0

        self.original_image = pygame.image.load("car.png").convert()
        self.image = self.original_image  # This will reference the rotated image.
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect().move(self.x, self.y)

        self.angle = math.radians(180)
        self.soll_angle = self.angle

        self.dvel = 1
        self.vel = 0
        self.velX = 0
        self.velY = 0
        self.maxvel = 15  # before 15

        self.angle = math.radians(180)
        self.soll_angle = self.angle

        self.pt1 = myPoint(self.pt.x - self.width / 2, self.pt.y - self.height / 2)
        self.pt2 = myPoint(self.pt.x + self.width / 2, self.pt.y - self.height / 2)
        self.pt3 = myPoint(self.pt.x + self.width / 2, self.pt.y + self.height / 2)
        self.pt4 = myPoint(self.pt.x - self.width / 2, self.pt.y + self.height / 2)

        self.p1 = self.pt1
        self.p2 = self.pt2
        self.p3 = self.pt3
        self.p4 = self.pt4

        self.distances = []

    def action(self, choice):
        if choice == 0:
            pass
        elif choice == 1:
            self.accelerate(self.dvel)
        elif choice == 8:
            self.accelerate(self.dvel)
            self.turn(1)
        elif choice == 7:
            self.accelerate(self.dvel)
            self.turn(-1)
        elif choice == 4:
            self.accelerate(-self.dvel)
        elif choice == 5:
            self.accelerate(-self.dvel)
            self.turn(1)
        elif choice == 6:
            self.accelerate(-self.dvel)
            self.turn(-1)
        elif choice == 3:
            self.turn(1)
        elif choice == 2:
            self.turn(-1)
        pass

    def accelerate(self, dvel):
        dvel = dvel * 2

        self.vel = self.vel + dvel

        if self.vel > self.maxvel:
            self.vel = self.maxvel

        if self.vel < -self.maxvel:
            self.vel = -self.maxvel

    def turn(self, dir):
        self.soll_angle = self.soll_angle + dir * math.radians(15)

    def update(self):

        # drifting code

        # if(self.soll_angle > self.angle):
        #     if(self.soll_angle > self.angle + math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)):
        #         self.angle = self.angle + math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)
        #     else:
        #         self.angle = self.soll_angle

        # if(self.soll_angle < self.angle):
        #     if(self.soll_angle < self.angle - math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)):
        #         self.angle = self.angle - math.radians(10) * self.maxvel / ((self.velX**2 + self.velY**2)**0.5 + 1)
        #     else:
        #         self.angle = self.soll_angle

        self.angle = self.soll_angle

        vec_temp = rotate(myPoint(0, 0), myPoint(0, self.vel), self.angle)
        self.velX, self.velY = vec_temp.x, vec_temp.y

        self.x = self.x + self.velX
        self.y = self.y + self.velY

        self.rect.center = self.x, self.y

        self.pt1 = myPoint(self.pt1.x + self.velX, self.pt1.y + self.velY)
        self.pt2 = myPoint(self.pt2.x + self.velX, self.pt2.y + self.velY)
        self.pt3 = myPoint(self.pt3.x + self.velX, self.pt3.y + self.velY)
        self.pt4 = myPoint(self.pt4.x + self.velX, self.pt4.y + self.velY)

        self.p1, self.p2, self.p3, self.p4 = rotateRect(self.pt1, self.pt2, self.pt3, self.pt4, self.soll_angle)

        self.image = pygame.transform.rotate(self.original_image, 90 - self.soll_angle * 180 / math.pi)
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)