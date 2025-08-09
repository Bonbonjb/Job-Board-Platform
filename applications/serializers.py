from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'user', 'cover_letter', 'resume',
            'created_at', 'status'
        ]
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context['request']

        if 'status' in validated_data:
            # If the current user is the applicant
            if request.user == instance.user:
                # Applicants can only withdraw their application
                if validated_data['status'] != 'withdrawn':
                    validated_data.pop('status')

            # If the current user is not the job poster
            elif request.user != instance.job.posted_by:
                # Remove status change if they are neither applicant nor poster
                validated_data.pop('status')

        return super().update(instance, validated_data)

