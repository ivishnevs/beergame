from django.db import models
from django.contrib.auth.models import User
import json


class Game(models.Model):
    name = models.CharField(u'Имя игры', max_length=30)
    steps_number = models.IntegerField(u'Продолжительность игры')
    current_step = models.IntegerField(u'Текущий шаг', default=1)
    gamer_count = models.IntegerField(u'Количество играков')
    total_fine = models.FloatField(default=0)
    holding_cost = models.FloatField(default=0.5)
    backorder_cost = models.FloatField(default=1)
    demand_pattern = models.IntegerField(default=1)

    creation_datetime = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    user = models.ForeignKey(User)

    def __str__(self):
        return "%s\'s %s game." % (self.user, self.name)

    @staticmethod
    def demand_func(step, pattern=demand_pattern):
        if pattern == 1:
            if step > 6:
                return 8
            if step < 4:
                return 6
            if step == 4:
                return 8
            if step == 5:
                return 11
            if step == 6:
                return 12
        else:
            return 8

    def is_step_finished(self):
        flag = True
        gamers = self.gamer_set.all()
        for gamer in gamers:
            if not gamer.is_step_completed:
                flag = False
        if flag:
            for gamer in gamers:
                order_list = gamer.get_order_list()
                supply_list = gamer.get_supply_list()
                gamer.current_order += order_list.pop(0)
                gamer.storage += supply_list.pop(0)
                gamer.set_order_list(order_list)
                gamer.set_supply_list(supply_list)
                gamer.is_step_completed = False
                gamer.save()
            self.current_step += 1
            self.save()

    def create_gamers(self):
        # settings
        saler = 'saler'
        fabrica = 'fabrica'
        distributor = 'distributor'

        gamer_list = []
        if self.gamer_set:
            for gamer in self.gamer_set.all():
                gamer.delete()

        for v in range(self.gamer_count):
            gamer = Gamer(game=self)
            if v is 0:
                gamer.role = saler
            elif v is self.gamer_count - 1:
                gamer.role = fabrica
            else:
                gamer.role = distributor + " #" + str(v)
            gamer.save()
            gamer_list.append(gamer)

        for i in range(1, self.gamer_count):
            prev_gamer = gamer_list[i-1]
            gamer = gamer_list[i]
            prev_gamer.supplier = gamer
            gamer.customer = prev_gamer
            prev_gamer.save()
            gamer.save()


class Gamer(models.Model):
    role = models.CharField(u'Игровая роль', default='role', max_length=30)
    supplier = models.OneToOneField('self', related_name='sup', blank=True, null=True)    # Поставщик
    customer = models.OneToOneField('self', related_name='cus', blank=True, null=True)    # Заказчик
    order_list = models.CharField(u'Список заказов', default='[6]', max_length=300)
    supply_list = models.CharField(u'Список поставок', default='[6]', max_length=300)
    storage = models.IntegerField(u'Склад', default=12)
    current_order = models.IntegerField(u'Текущий заказ', default=6)
    penalty = models.FloatField(u'Штраф', default=0)
    active = models.BooleanField(default=False)
    is_step_completed = models.BooleanField(default=False)
    game = models.ForeignKey(Game)

    def __str__(self):
        return "%s of %s game." % (self.role, self.game_id)

    def complete_step(self):
        self.is_step_completed = True
        self.save()
        self.game.is_step_finished()

    def get_order_list(self):
        return json.loads(self.order_list)

    def get_supply_list(self):
        return json.loads(self.supply_list)

    def set_order_list(self, val):
        self.order_list = json.dumps(val)

    def set_supply_list(self, val):
        self.supply_list = json.dumps(val)

    def set_order(self, val):
        order_list = self.get_order_list()
        order_list.append(val)
        self.set_order_list(order_list)
        self.save()

    def set_supply(self, val):
        supply_list = self.get_supply_list()
        supply_list.append(val)
        self.set_supply_list(supply_list)
        self.save()

    def make_order(self, val):
        if self.supplier:
            self.supplier.set_order(val)
        else:
            self.set_supply(val)
            self.save()
        if not self.customer:   # Добавлено для генерации спроса saler'у
            step = self.game.current_step
            demand = self.game.demand_func(step)
            self.set_order(demand)
            self.save()

    def make_supply(self):
        if self.storage >= self.current_order:
            supply = self.current_order
            self.storage -= self.current_order
            self.current_order = 0

            self.penalty += self.storage * self.game.holding_cost  # holding_cost = 0.5
        else:
            supply = self.storage
            self.current_order -= self.storage
            self.storage = 0
            self.penalty += self.current_order * self.game.backorder_cost  # backorder_cost = 1
        if self.customer:
            self.customer.set_supply(supply)
        self.save()

    def record_stats(self):
        step = self.game.current_step
        current_order = self.current_order
        if self.supplier:
            my_order = self.supplier.get_order_list()[-1]
        else:
            my_order = self.get_supply_list()[-1]
        storage = self.storage
        penalty = self.penalty
        Stats.objects.create(gamer=self, step=step, current_order=current_order,
                             my_order=my_order, storage=storage, penalty=penalty)


class Stats(models.Model):
    gamer = models.ForeignKey(Gamer)
    step = models.IntegerField(u'# хода')
    current_order = models.IntegerField(u'Текущий заказ')
    my_order = models.IntegerField(u'Мой заказ')
    storage = models.IntegerField(u'Склад')
    penalty = models.FloatField(u'Штраф')
