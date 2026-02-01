import pandas as pd
import io
import json
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import EquipmentBatch
from .serializers import UserSerializer, EquipmentBatchSerializer
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UploadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle CSV Upload.
        1. Validate Column Headers
        2. Parse with Pandas
        3. Save Statistics
        4. Maintain max 5 records history
        """
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided. Please attach a CSV file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read CSV
            df = pd.read_csv(file_obj)
            
            # 1. Validation: Check Columns
            required_cols = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                return Response(
                    {'error': f'Invalid CSV format. Missing columns: {", ".join(missing_cols)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Analytics: Calculate Required Parameters
            total_count = len(df)
            avg_flowrate = df['Flowrate'].mean()
            avg_pressure = df['Pressure'].mean()
            avg_temperature = df['Temperature'].mean()
            # Convert counts to dict for JSON storage
            type_distribution = df['Type'].value_counts().to_dict()

            # 3. Save: Create new batch record
            batch = EquipmentBatch.objects.create(
                file_name=file_obj.name,
                total_count=total_count,
                avg_flowrate=avg_flowrate,
                avg_pressure=avg_pressure,
                avg_temperature=avg_temperature,
                type_distribution=type_distribution
            )

            # 4. History Retention: Keep only latest 5
            # We get IDs of the newest 5 (ordered by -uploaded_at)
            recent_ids = EquipmentBatch.objects.order_by('-uploaded_at').values_list('id', flat=True)[:5]
            # Delete anything NOT in that list
            EquipmentBatch.objects.exclude(id__in=recent_ids).delete()

            return Response(EquipmentBatchSerializer(batch).data, status=status.HTTP_201_CREATED)

        except pd.errors.EmptyDataError:
             return Response({'error': 'The uploaded CSV file is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f"Processing Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class SummaryView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EquipmentBatchSerializer

    def get_object(self):
        return EquipmentBatch.objects.first()

class HistoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EquipmentBatchSerializer
    queryset = EquipmentBatch.objects.all()[:5]

class ReportView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        batch = EquipmentBatch.objects.first()
        if not batch:
            return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{batch.id}.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        y = 750
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, y, "Chemical Equipment Analysis Report")
        y -= 30
        p.setFont("Helvetica", 12)
        p.drawString(100, y, f"File Name: {batch.file_name}")
        y -= 20
        p.drawString(100, y, f"Date: {batch.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 30
        
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "Summary Statistics")
        y -= 25
        p.setFont("Helvetica", 12)
        p.drawString(120, y, f"Total Equipment Count: {batch.total_count}")
        y -= 20
        p.drawString(120, y, f"Average Flowrate: {batch.avg_flowrate:.2f}")
        y -= 20
        p.drawString(120, y, f"Average Pressure: {batch.avg_pressure:.2f}")
        y -= 20
        p.drawString(120, y, f"Average Temperature: {batch.avg_temperature:.2f}")
        
        y -= 40
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, y, "Equipment Type Distribution")
        y -= 25
        p.setFont("Helvetica", 12)
        
        # dist is a dict
        if isinstance(batch.type_distribution, str):
             dist = json.loads(batch.type_distribution)
        else:
             dist = batch.type_distribution

        for eq_type, count in dist.items():
            p.drawString(120, y, f"{eq_type}: {count}")
            y -= 20
            
        p.showPage()
        p.save()
        return response
