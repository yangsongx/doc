#coding=utf-8
from django import forms

from models import (AccountProfile,GENDER_CHOICES)

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

        print  self.cleaned_data['address']
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