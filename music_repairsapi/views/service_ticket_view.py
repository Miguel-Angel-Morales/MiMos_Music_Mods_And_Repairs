"""View module for handling requests for service_ticket data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from music_repairsapi.models import ServiceTicket, Employee, Customer, Instrument
from django.utils import timezone


class ServiceTicketView(ViewSet):
    """MiMos Music Mods and Repairs API service_ticket_view"""

    def list(self, request):
        """Handle GET requests to get all service_tickets

        Returns:
            Response -- JSON serializer list of service_tickets
        """
        service_tickets = []

        if request.auth.user.is_staff:
            service_tickets = ServiceTicket.objects.all()

            if "status" in request.query_params:
                if request.query_params['status'] == "done":
                    service_tickets = service_tickets.filter(
                        date_completed__isnull=False)

                if request.query_params['status'] == "all":
                    pass

        else:
            service_tickets = ServiceTicket.objects.filter(
                customer__user=request.auth.user)

        serializer = ServiceTicketSerializer(service_tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single service_ticket

        Returns:
            Response -- JSON serializer service_ticket record
        """

        service_ticket = ServiceTicket.objects.get(pk=pk)
        serializer = ServiceTicketSerializer(
            service_ticket, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serializer representation of newly created service ticket
        """
        customer = Customer.objects.get(user=request.auth.user)

        # Assuming you have a user field in your Employee model to link it to the User model

        instrument_pk = request.data.get('instrument')
        
        try:
            instrument = Instrument.objects.get(pk=instrument_pk)
        except Instrument.DoesNotExist:
            return Response({"error": "Instrument with the given ID does not exist."}, status=status.HTTP_404_NOT_FOUND)

        new_ticket = ServiceTicket(
            customer=customer,
            instrument=instrument,
            description=request.data['description'],
            notes=request.data['notes'],
            date=request.data["date"],
            modification=request.data['modification'],
            repair=request.data['repair'],
            setup=request.data['setup'],
            priority=request.data['priority']
        )

        # Save the new service ticket
        new_ticket.save()

        serializer = ServiceTicketSerializer(new_ticket, many=False)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



    def update(self, request, pk=None):
        # "Handle Put request for single customer"

        # Returns:
        # Response -- No response body. Just 204 status code.

        # Select the targeted Ticket using PK
        ticket = ServiceTicket.objects.get(pk=pk)
        # Get the employee id from the client request
        employee_id = request.data['employee']
        # Select the employee from the database using that id
        assigned_employee = Employee.objects.get(pk=employee_id)
        # Assign the Employee instance to the employee property to the ticket
        ticket.employee = assigned_employee
        # Save the updated ticket
        ticket.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for single service_ticket

        Returns:
            Response -- None with 204 status code
        """

        service_ticket = ServiceTicket.objects.get(pk=pk)
        service_ticket.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


# For customers to see the Full_name property
class TicketEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'user', 'specialty')


# For employees to see the Full_name property
class TicketCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'user')


class ServiceTicketSerializer(serializers.ModelSerializer):
    """JSON serializer for service_ticket"""
    employee = TicketEmployeeSerializer(many=False)
    customer = TicketCustomerSerializer(many=False)


    class Meta:
        model = ServiceTicket
        fields = ('id', 'customer', 'employee', 'instrument', 'description', 'notes', 'date', 'modification', 'repair',
                    'setup', 'priority')
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['date'] = instance.date.strftime('%Y-%m-%d')  # Format the date
        return data
