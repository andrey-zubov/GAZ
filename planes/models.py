from django.db import models
from django.contrib.auth.models import User


class Curator(models.Model):
    class Meta:
        verbose_name = "Куратор"
        verbose_name_plural = "Кураторы"

    title = models.CharField(
        max_length=120,
        verbose_name="Куратор"
    )

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'

class UserTypes(models.Model):
    class Meta:
        verbose_name = "Тип пользователя"
        verbose_name_plural = "Типы пользователя"

    title = models.CharField(
        max_length=120,
        verbose_name="Тип пользователя (Администратор, Куратор, БПиЭА, Пользователь)"
    )


class UserSub(models.Model):
    group = models.ForeignKey(
        UserTypes,
        verbose_name="Группа пользователей",
        on_delete=models.DO_NOTHING
    )
    title = models.CharField(
        max_length=150,
        verbose_name="Подтип обычных пользователей (Экономист, специалист АСЭЗ, Юрист)",
        blank=True,
        null=True
    )


class CustomUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name="Пользователь")
    curator = models.ForeignKey(
        Curator,
        verbose_name="Подразделение (Куратор)",
        on_delete=models.DO_NOTHING
    )
    email = models.EmailField()
    name = models.CharField(
        max_length=150,
        verbose_name="Фамилия, Имя, Отчество"
    )
    position = models.CharField(
        max_length=200,
        verbose_name="Должность",
        null=True,
        blank=True
    )
    user_type = models.ForeignKey(
        UserTypes,
        verbose_name="Тип пользователя (Пользователь, Администратор, Куратор, Суперпользователь, БПиЭА)",
        on_delete=models.DO_NOTHING
    )
    user_sub_type = models.ForeignKey(
        UserSub,
        verbose_name="Подтип пользователей (Юрист, специалист АСЭЗ, Экономист)",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )


class UserActivityJournal(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.DO_NOTHING)
    date_time_of_activity = models.DateTimeField()
    activity = models.CharField(
        max_length=200,
        verbose_name="Действия пользователя в системе",
        blank=True,
        null=True
    )
    clicks = models.PositiveIntegerField(
        verbose_name="Количество кликов пользователя",
        blank=True,
        null=True
    )
    activity_system_module = models.CharField(
        max_length=100,
        verbose_name="Раздел системы",
        blank=True
    )


class FinanceCosts(models.Model):
    class Meta:
        verbose_name = "Статья финансирования"
        verbose_name_plural = "Статьи финансирования"
    title = models.CharField(
        verbose_name="Название статьи",
        max_length=100
    )

    def __str__(self):
        try:
            return str(self.title)
        except:
            return 'Ошибка в данных'



class PurchaseType(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Вид закупки (Конкурентная, неконкурентная)"
    )


class ActivityForm(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Вид деятельности"
    )


class StateASEZ(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Состояние АСЭЗ"
    )


class NumberPZTRU(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Номер пункта ПоЗТРУ"
    )


class ContractStatus(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Статус договора"
    )


class Currency(models.Model):
    title = models.CharField(
        max_length=10,
        verbose_name="Валюта"
    )


class ContractType(models.Model):
    title = models.CharField(
        max_length=150,
        help_text="Тип договора(Центр, Филиал)"
    )


class ContractMode(models.Model):
    title = models.CharField(
        max_length=150,
        help_text="Вид договора (Основной, доп.соглашение)"
    )


class Counterpart(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Контрагент"
    )
    email = models.EmailField()
    reg_addr = models.CharField(max_length=255)
    UNP = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)


class Contract(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="наименование договора"
    )
    finance_cost = models.ForeignKey(
        FinanceCosts,
        on_delete=models.DO_NOTHING,
        verbose_name="статья финансирования")
    curator = models.ForeignKey(
        Curator,
        on_delete=models.DO_NOTHING,
        verbose_name="Куратор"
    )
    contract_type = models.ForeignKey(
        ContractType,
        verbose_name="Тип договора",
        on_delete=models.DO_NOTHING,
        help_text="филиал или центръ"
    )
    contract_mode = models.ForeignKey(
        ContractMode,
        verbose_name="Вид договора",
        on_delete=models.DO_NOTHING,
        help_text="основной либо доп.согл.")
    purchase_type = models.ForeignKey(
        PurchaseType,
        verbose_name="тип закупки",
        on_delete=models.DO_NOTHING,
        help_text="Вид закупки (конкурентная, неконкурентная)"
    )
    activity_form = models.ForeignKey(
        ActivityForm,
        verbose_name="вид деятельности",
        on_delete=models.DO_NOTHING
    )
    stateASEZ = models.ForeignKey(
        StateASEZ,
        verbose_name="автоматизированая система эллектронных закупок",
        on_delete=models.DO_NOTHING
    )
    number_ppz = models.CharField(
        max_length=150,
        verbose_name="номер позиция плана закупок",
        null=True,
        blank=True
    )
    number_PZTRU = models.ForeignKey(
        NumberPZTRU,
        verbose_name="ПЗТРУ",
        help_text="положение о закупках товаров, работ, услуг",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    contract_status = models.ForeignKey(
        ContractStatus,
        verbose_name="статус договора",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )
    plan_load_date_ASEZ = models.DateField(
        verbose_name="планируемая дата загрузки в АСЭЗ",
    )
    fact_load_date_ASEZ = models.DateField(
        verbose_name="фактическая дата загрузки в АСЭЗ",
        null=True,
        blank=True
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    number_KGG = models.CharField(
        max_length=100,
        verbose_name="номер договора от центрального органа",
        null=True,
        blank=True
    )
    register_number_SAP = models.CharField(
        max_length=100,
        verbose_name="Регистрационный номер в САП",
        null=True,
        blank=True
    )
    contract_number = models.CharField(
        max_length=100,
        verbose_name="Номер договора",
        null=True,
        blank=True
    )
    plan_sign_date = models.DateField()
    fact_sign_date = models.DateField(
        null=True,
        blank=True
    )
    start_date = models.DateField(
        verbose_name="дата начала контракта"
    )
    end_time = models.DateField(
        verbose_name="дата окончания",
        null=True, blank=True
    )
    counterpart = models.ForeignKey(
        Counterpart,
        on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # TODO   contract_mode


class SumsRUR(models.Model):
    contract = models.ForeignKey(
        Contract,
        verbose_name="Контракт",
        on_delete=models.DO_NOTHING
    )
    start_max_price_ASEZ_NDS = models.PositiveIntegerField(
        verbose_name="стартовая цена АСЭЗ с НДС ",
        null=True,
        blank=True
    )
    currency_rate_on_load_date_ASEZ_NDS = models.FloatField(
        verbose_name="Курс валюты на дату загрузки в бел.руб.",
        null=True,
        blank=True
    )
    contract_sum_NDS_RUB = models.FloatField(
        verbose_name="Сумма договора с НДС рос.руб.",
        blank=True,
        null=True
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name="Валюта",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    delta_data_ASEZ = models.FloatField(
        verbose_name="Отклонение от НМЦ в АСЭЗ",
        blank=True,
        null=True
    )


class SumsBYN(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.DO_NOTHING)
    year = models.DateField()
    plan_sum_SAP = models.FloatField(
        verbose_name="Плановая сумма САП",
        blank=True,
        null=True
    )
    contract_sum_without_NDS_BYN = models.FloatField(
        verbose_name="Сумма всего договора без НДС",
        default=0
    )
    contract_sum_with_NDS_BYN = models.FloatField(
        verbose_name="Сумма договора с НДС бел.руб.",
        blank=True,
        null=True
    )
    contract_total_sum_with_sub_BYN = models.FloatField(
        verbose_name='Общая сумма договора всего с доп соглашениями, б.р. без ндс',
        null=True,
        blank=True,
    )
    forecast_total = models.FloatField(
        verbose_name='Прогноз, всего',
        blank=True,
        null=True
    )
    economy_total = models.FloatField(
        verbose_name='Экономия по заключенному договору, всего',
        blank=True,
        null=True
    )
    fact_total = models.FloatField(
        verbose_name='Факт, всего',
        blank=True,
        null=True
    )
    economy_contract_result = models.FloatField(
        verbose_name='Экономия по результатам исполнения договоров всего',
        blank=True,
        null=True
    )
    total_sum_unsigned_contracts = models.FloatField(
        verbose_name='Сумма средств по незаключенным договорам',
        blank=True,
        null=True
    )
    economy_total_absolute = models.FloatField(
        verbose_name='Абсолютная экономия по договору, всего',
        blank=True,
        null=True
    )


class Planning(models.Model):
    class QuartChoices:
        ch = [(1, 'I'), (2, 'II'), (2, 'III'), (4, 'IV')]
    class Meta:
        verbose_name = "План"
        verbose_name_plural = "Планы"

    FinanceCosts = models.ForeignKey(
        FinanceCosts,
        verbose_name="Статья финансирования",
        on_delete=models.DO_NOTHING
    )
    curator = models.ForeignKey(
        Curator,
        verbose_name="Куратор",
        on_delete=models.DO_NOTHING
    )
    year = models.DateField(
        verbose_name="Год"
    )
    period = models.DateField(
        verbose_name="Период"
    )
    total = models.FloatField(
        verbose_name="Сумма, Лимит средств",
        default=0
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name="Валюта",
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        try:
            return ('Планирование по ст %s на %s год, куратор %s'
                    % (self.FinanceCosts, self.year, self.curator))
        except:
            return 'Ошибка в данных'




