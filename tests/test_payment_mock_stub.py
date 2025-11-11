import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from unittest.mock import Mock, patch
from services.payment_service import PaymentGateway
from services.library_service import pay_late_fees, refund_late_fee_payment


class TestPayLateFees:
    """Test cases for pay_late_fees function using mocks."""

    @patch('services.library_service.calculate_late_fee_for_book')
    @patch('services.library_service.get_book_by_id')
    def test_successful_payment(self, mock_get_book, mock_calc_fee):
        """Test successful payment processing."""
        # Mock the fee calculation
        mock_calc_fee.return_value = {'fee_amount': 5.00, 'days_overdue': 5, 'status': 'OK'}
        # Mock the book lookup
        mock_get_book.return_value = {'title': 'Test Book', 'available_copies': 5}

        # Create mock gateway
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.return_value = (True, "txn_123456_1234567890", "Payment of $5.00 processed successfully")

        # Call function with mock
        success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)

        # Assertions
        assert success == True
        assert "Payment successful" in message
        assert transaction_id == "txn_123456_1234567890"
        mock_gateway.process_payment.assert_called_once_with(
            patron_id="123456",
            amount=5.00,
            description="Late fees for 'Test Book'"
        )

    @patch('services.library_service.calculate_late_fee_for_book')
    @patch('services.library_service.get_book_by_id')
    def test_payment_declined_by_gateway(self, mock_get_book, mock_calc_fee):
        """Test payment declined by gateway."""
        # Mock the fee calculation
        mock_calc_fee.return_value = {'fee_amount': 5.00, 'days_overdue': 5, 'status': 'OK'}
        # Mock the book lookup
        mock_get_book.return_value = {'title': 'Test Book', 'available_copies': 5}

        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.return_value = (False, "", "Payment declined: insufficient funds")

        success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)

        assert success == False
        assert "Payment failed: Payment declined: insufficient funds" == message
        assert transaction_id is None
        mock_gateway.process_payment.assert_called_once()

    def test_invalid_patron_id_mock_not_called(self):
        """Test invalid patron ID - mock should not be called."""
        mock_gateway = Mock(spec=PaymentGateway)

        success, message, transaction_id = pay_late_fees("12345", 1, mock_gateway)  # Invalid: 5 digits

        assert success == False
        assert "Invalid patron ID" in message
        assert transaction_id is None
        mock_gateway.process_payment.assert_not_called()

    @patch('services.library_service.calculate_late_fee_for_book')
    @patch('services.library_service.get_book_by_id')
    def test_zero_late_fees_mock_not_called(self, mock_get_book, mock_calc_fee):
        """Test zero late fees - mock should not be called."""
        # Mock the fee calculation to return 0
        mock_calc_fee.return_value = {'fee_amount': 0.00, 'days_overdue': 0, 'status': 'OK'}
        # Mock the book lookup
        mock_get_book.return_value = {'title': 'Test Book', 'available_copies': 5}

        mock_gateway = Mock(spec=PaymentGateway)

        success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)

        assert success == False
        assert "No late fees to pay" in message
        assert transaction_id is None
        mock_gateway.process_payment.assert_not_called()

    @patch('services.library_service.calculate_late_fee_for_book')
    @patch('services.library_service.get_book_by_id')
    def test_network_error_exception_handling(self, mock_get_book, mock_calc_fee):
        """Test network error exception handling."""
        # Mock the fee calculation
        mock_calc_fee.return_value = {'fee_amount': 5.00, 'days_overdue': 5, 'status': 'OK'}
        # Mock the book lookup
        mock_get_book.return_value = {'title': 'Test Book', 'available_copies': 5}

        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.side_effect = Exception("Network timeout")

        success, message, transaction_id = pay_late_fees("123456", 1, mock_gateway)

        assert success == False
        assert "Payment processing error: Network timeout" == message
        assert transaction_id is None
        mock_gateway.process_payment.assert_called_once()


class TestRefundLateFeePayment:
    """Test cases for refund_late_fee_payment function using mocks."""

    def test_successful_refund(self):
        """Test successful refund processing."""
        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.refund_payment.return_value = (True, "Refund of $5.00 processed successfully. Refund ID: refund_txn_123_1234567890")

        success, message = refund_late_fee_payment("txn_123", 5.00, mock_gateway)

        assert success == True
        assert "Refund of $5.00 processed successfully" in message
        mock_gateway.refund_payment.assert_called_once_with("txn_123", 5.00)

    def test_invalid_transaction_id_rejection(self):
        """Test invalid transaction ID rejection."""
        mock_gateway = Mock(spec=PaymentGateway)

        success, message = refund_late_fee_payment("invalid_txn", 5.00, mock_gateway)

        assert success == False
        assert "Invalid transaction ID." == message
        mock_gateway.refund_payment.assert_not_called()

    def test_invalid_refund_amount_negative(self):
        """Test invalid refund amount - negative."""
        mock_gateway = Mock(spec=PaymentGateway)

        success, message = refund_late_fee_payment("txn_123", -5.00, mock_gateway)

        assert success == False
        assert "Refund amount must be greater than 0." == message
        mock_gateway.refund_payment.assert_not_called()

    def test_invalid_refund_amount_zero(self):
        """Test invalid refund amount - zero."""
        mock_gateway = Mock(spec=PaymentGateway)

        success, message = refund_late_fee_payment("txn_123", 0.00, mock_gateway)

        assert success == False
        assert "Refund amount must be greater than 0." == message
        mock_gateway.refund_payment.assert_not_called()

    def test_invalid_refund_amount_exceeds_maximum(self):
        """Test invalid refund amount - exceeds $15 maximum."""
        mock_gateway = Mock(spec=PaymentGateway)

        success, message = refund_late_fee_payment("txn_123", 20.00, mock_gateway)

        assert success == False
        assert "Refund amount exceeds maximum late fee." == message
        mock_gateway.refund_payment.assert_not_called()
