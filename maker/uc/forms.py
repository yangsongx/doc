#coding=utf-8
from django import forms

from models import (AccountProfile,CorpusData,Robot,GENDER_CHOICES)

class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(EditProfileForm, self).__init__(*args, **kw)

        acccount_profile = self.instance;
        self.fields['phone_number'].required = False
        self.fields['phone_number'].initial = acccount_profile.phone_number

        self.fields['email'] = forms.CharField(max_length=24)
        self.fields['email'].required = False
        self.fields['email'].initial = acccount_profile.user.email

        self.fields['address'].required = False
        self.fields['address'].initial = acccount_profile.address

        self.fields['nickname'].required = False
        self.fields['nickname'].initial = acccount_profile.nickname

        self.fields['gender'] = forms.ChoiceField(choices=GENDER_CHOICES)
        self.fields['gender'].initial = acccount_profile.gender

        self.fields['username'] =  forms.CharField(max_length=24)
        self.fields['username'].required = False
        self.fields['username'].initial = acccount_profile.user.username

    class Meta:
        model = AccountProfile
        #fields = ('phone_number', 'address','nickname', 'gender','user')
        # exclude = {'mail_act','mail_act_expire'}
        exclude = ['user']

    def save(self):

        # acccount_profile = super(EditProfileForm, self).save(commit=False)
        # user = self.instance.user#User.objects.get(pk=idx)
        accout_uprofile = self.instance#AccountProfile.objects.get(user_id =  user.id)
        accout_uprofile.address = self.cleaned_data['address']
        accout_uprofile.phone_number = self.cleaned_data['phone_number']
        accout_uprofile.nickname = self.cleaned_data['nickname']
        accout_uprofile.gender = self.cleaned_data['gender']

        # user.email = self.cleaned_data['email']
        # user.username = self.cleaned_data['username']

        accout_uprofile.save()

        # accout_uprofile.user = user.save();
        return accout_uprofile

class CorpusForm(forms.ModelForm):

    class Meta:
        model = CorpusData
        fields = ('question', 'answer')

    def clean_question(self):
        question = self.cleaned_data['question']
        if  question == '':
            raise forms.ValidationError('问题不能为空')
        return question
    def clean_answer(self):
        answer = self.cleaned_data['answer']
        if  answer == '':
            raise forms.ValidationError('答案不能为空')
        return answer

    def save(self, user):
        c_obj = CorpusData()
        c_obj.question = self.cleaned_data['question']
        c_obj.answer = self.cleaned_data['answer']
        c_obj.owner = user
        c_obj.save()

class RobotInfoForm(forms.ModelForm):
    def __init__(self, *args, **kw):
        super(RobotInfoForm, self).__init__(*args, **kw)

        robj = self.instance;
        self.fields['rob_alias'].required = False
        self.fields['rob_alias'].initial = robj.rob_alias

        self.fields['rob_gender'] = forms.ChoiceField(choices=GENDER_CHOICES)
        self.fields['rob_gender'].initial = robj.rob_sex

        self.fields['rob_age'].required = False
        self.fields['rob_age'].initial = robj.rob_age

    class Meta:
        model = Robot
        exclude = ['owner']

    def save(self):

        robj = self.instance
        robj.rob_alias= self.cleaned_data['rob_alias']
        robj.rob_sex= self.cleaned_data['rob_gender']
        robj.rob_age= self.cleaned_data['rob_age']

        robj.save()

        return robj
