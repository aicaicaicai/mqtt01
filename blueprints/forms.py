# 数据验证模块
import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(
        validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='邮箱不能为空')])
    captcha = wtforms.StringField(
        validators=[Length(4, 4, message='请输入正确的验证码'), InputRequired(message='验证码不能为空')])
    username = wtforms.StringField(
        validators=[Length(2, 20, message='请输入正确的用户名'), InputRequired(message='用户名不能为空')])
    password = wtforms.StringField(
        validators=[Length(6, 20, message='请输入正确的密码'), InputRequired(message='密码不能为空')])
    password_confirm = wtforms.StringField(
        validators=[EqualTo('password', message='两次密码不一致'), InputRequired(message='请再次输入密码')])

    # 自定义验证函数
    # 1. 邮箱是否已经注册
    def validate_email(self, field):
        # field.data: 获取邮箱
        # self.email.data: 获取邮箱
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='该邮箱已经注册')

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        # field.data: 获取验证码
        # self.captcha.data: 获取验证码
        # self代表当前的form对象
        captcha = field.data
        email = self.email.data
        email_captcha = EmailCaptchaModel.query.filter_by(email=email).order_by(
            EmailCaptchaModel.create_time.desc()).first()
        if not email_captcha or email_captcha.captcha != captcha:
            raise wtforms.ValidationError(message='验证码错误')
        # else:
        #     # todo: 验证码是否过期, 目前方法是将验证码存储在数据库中，后期可以考虑将验证码存储在redis中，或者设置脚本每日清理过期验证码
        #     # 验证码正确, 删除已用验证码
        #     # 删除数据库中超过15分钟的验证码(验证是否存在)
        #     email_captchas = EmailCaptchaModel.query.filter(EmailCaptchaModel.create_time < datetime.datetime.now() - datetime.timedelta(minutes=15)).all()
        #     if not email_captchas:
        #         db.session.delete(email_captcha)
        #         db.session.delete(email_captchas)
        #     else:
        #         db.session.delete(email_captcha)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(
        validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='邮箱不能为空')])
    password = wtforms.StringField(
        validators=[Length(6, 20, message='请输入正确的密码'), InputRequired(message='密码不能为空')])


class DeviceForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(2, 40, message='请输入正确的设备名称'), InputRequired(message='设备名称不能为空')])
    type = wtforms.StringField(validators=[Length(2, 40, message='请输入正确的设备类型'), InputRequired(message='设备类型不能为空')])
    # device_model = wtforms.StringField(validators=[Length(2, 40, message='请输入正确的设备型号'), InputRequired(message='设备型号不能为空')])
    # device_sn = wtforms.StringField(
    #     validators=[Length(2, 40, message='请输入正确的设备序列号'), InputRequired(message='设备序列号不能为空')])
    # device_ip = wtforms.StringField(
    #     validators=[Length(2, 40, message='请输入正确的设备IP'), InputRequired(message='设备IP不能为空')])
    # device_port = wtforms.IntegerField(validators=[InputRequired(message='设备端口不能为空')])
    description = wtforms.StringField(validators=[Length(min=2, message='请输入正确的设备描述'), InputRequired(message='设备描述不能为空')])
    # status = wtforms.IntegerField(validators=[InputRequired(message='设备状态不能为空')])


class MessageForm(wtforms.Form):
    topic = wtforms.StringField(validators=[Length(min=2, max=40, message='请输入正确的主题'), InputRequired(message='主题不能为空')])
    content = wtforms.StringField(
        validators=[Length(min=2, message='请输入正确的消息内容'), InputRequired(message='消息内容不能为空')])

class FactoryForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=2, max=40, message='请输入正确的厂商名称'), InputRequired(message='厂商名称不能为空')])
    address = wtforms.StringField(validators=[Length(min=2, max=40, message='请输入正确的厂商地址'), InputRequired(message='厂商地址不能为空')])
    description = wtforms.StringField(validators=[Length(min=2, message='请输入正确的厂商描述'), InputRequired(message='厂商描述不能为空')])

class ControlForm(wtforms.Form):
    factoryName = wtforms.StringField(validators=[Length(min=2, message='请选择设备所在的工厂名'), InputRequired(message='请选择设备所在的工厂名')])
    control = wtforms.StringField(validators=[Length(min=1, message='请输入正确的控制指令'), InputRequired(message='控制指令不能为空')])
    opt = wtforms.IntegerField(validators=[InputRequired(message='操作类型不能为空')])
