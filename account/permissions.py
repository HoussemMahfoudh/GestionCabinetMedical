from account.models import MyUser 
import rules.contrib.views

@rules.predicate
def is_patient(user, MyUser):
    return user.is_patient == True

@rules.predicate
def is_doctor(user, MyUser):
    return user.is_doctor == True

rules.add_rule('patient', is_patient)
rules.add_rule('doctor', is_doctor)