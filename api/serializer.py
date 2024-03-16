from rest_framework import serializers
from .models import CustomUser, Company, Owner, CompanyField, Branch, Supplier,Notes
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
                  'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data['password']
        password2 = data['password2']
        if password != password2:
            raise serializers.ValidationError('Passwords do\'nt match')
        else:
            return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        exclude = ['company']

    def update(self, instace, validated_data):
        instace.name = validated_data.get('name', instace.name)
        instace.owner_id = validated_data.get('owner_id',
                                              instace.owner_id)

        instace.owner_position = validated_data.get('onwer_position',
                                                    instace.onwer_position)

        instace.address = validated_data.get('address',
                                             instace.address)


class CompanyFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyField
        exclude = ['id', 'company']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ['company']


class CompanySerializer(serializers.ModelSerializer):
    owners = OwnerSerializer(many=True, required=False)
    company_fields = CompanyFieldSerializer(many=True)
    user = UserSerializer(many=False)
    supplier = SupplierSerializer(many=False, required=False)

    class Meta:
        model = Company
        fields = "__all__"

    def validate(self, data):
        password = data['user']['password']
        password2 = data['user']['password2']
        if password != password2:
            raise serializers.ValidationError('Passwords don\'t match')
        else:
            return data

    def create(self, validated_data):
        print("enter create function")
        # create user instance
        user = validated_data.pop('user')
        user.pop('password2')
        user = CustomUser.objects.create(**user)
        user.set_password(user.password)
        user.save()
        # create token for that user
        token = Token.objects.create(user=user)

        # extract other entities
        owners = validated_data.get('owners')
        if owners:
            validated_data.pop('owners')
        company_fields = validated_data.pop('company_fields')
        if validated_data.get('is_supplier'):
            supplier = validated_data.pop('supplier')
            company = Company.objects.create(**validated_data, user=user)
            supplier = Supplier.objects.create(**supplier,company=company)
        else:
            company = Company.objects.create(**validated_data, user=user)

        # iterate over owners and create each instance
        # print(owners)
        if owners:
            for owner in owners:
                Owner.objects.create(**owner, company=company)

        # iterate over fields and create instances
        for field in company_fields:
            CompanyField.objects.create(**field, company=company)

        # print(f'supplier is {validated_data.get("is_supplier")}')
        # if validated_data.get('is_supplier'):
        #     print(f"validated data is {validated_data} ")
        #     supplier = Supplier.objects.create(
        #         company=company,
        #     )
        # add token to the serializer
        company_data = CompanySerializer(company).data
        company_data['user']['token'] = token.key
        return company_data

    # def update(self, instace, validated_data):
    #     print('entered update method')
    #     instace.name = validated_data.get('name', instace.name)
    #     instace.location = validated_data.get('location', instace.name)
    #     instace.commercial_registration_number = validated_data.get(
    #         'commercial_registration_number',
    #         instace.commercial_registration_number)
    #     instace.tax_card_number = validated_data.get('tax_card_number',
    #                                                  instace.tax_card_number)
    #     instace.mobile = validated_data.get('mobile', instace.mobile)
    #     instace.landline = validated_data.get('landline', instace.landline)
    #     instace.fax_number = validated_data.get(
    #         'fax_number', instace.fax_number)
    #     instace.company_type = validated_data.get(
    #         'company_type', instace.company_type)
    #     instace.company_capital = validated_data.get(
    #         'company_capital', instace.company_capital)
    #     instace.save()

    #     owners = validated_data.get('owners')
    #     for owner in owners:
    #         owner_id = owner.get('id')
    #         if owner_id is None:
    #             print('owner id isn\'t found')
    #             Owner.objects.create(**owner)
    #         else:
    #             print(f"owner id is found and it = {owner_id}")
    #             owner_instance = Owner.objects.get(id=owner_id)
    #             serializer=OwnerSerializer(instance=owner_instance,data=owner)
    #             serializer.update(owner_instance,owner)
    #             owner_instance.save()
    #     return instace

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notes
        fields = '__all__'
