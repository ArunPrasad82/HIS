"""Billing controllers."""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from models.billing import Billing, BillingItem, Payment, BillingTax, BillingType, PaymentStatus, PaymentMode
from utils.generators import generate_invoice_number
from datetime import datetime, date
from decimal import Decimal


class BillingController:
    """Billing management controller."""

    def __init__(self, db: Session):
        """Initialize controller.
        
        Args:
            db: Database session
        """
        self.db = db

    def create_billing(self, hospital_id: int, billing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new billing/invoice.
        
        Args:
            hospital_id: Hospital ID
            billing_data: Billing data dictionary
            
        Returns:
            Created billing data
        """
        try:
            # Generate invoice number
            invoice_number = generate_invoice_number("HOS", "INV")
            
            # Calculate totals
            subtotal = Decimal(str(billing_data.get("subtotal", 0)))
            discount = Decimal(str(billing_data.get("discount_amount", 0)))
            tax_percentage = Decimal(str(billing_data.get("tax_percentage", 0)))
            
            # Calculate tax
            taxable_amount = subtotal - discount
            tax_amount = (taxable_amount * tax_percentage) / 100
            total_amount = taxable_amount + tax_amount
            
            billing = Billing(
                hospital_id=hospital_id,
                patient_id=billing_data["patient_id"],
                invoice_number=invoice_number,
                invoice_date=date.today(),
                admission_id=billing_data.get("admission_id"),
                appointment_id=billing_data.get("appointment_id"),
                billing_type=BillingType[billing_data["billing_type"].upper()],
                panel_id=billing_data.get("panel_id"),
                consultation_fee=Decimal(str(billing_data.get("consultation_fee", 0))),
                procedures_cost=Decimal(str(billing_data.get("procedures_cost", 0))),
                medicines_cost=Decimal(str(billing_data.get("medicines_cost", 0))),
                investigation_cost=Decimal(str(billing_data.get("investigation_cost", 0))),
                bed_charge=Decimal(str(billing_data.get("bed_charge", 0))),
                accommodation_charge=Decimal(str(billing_data.get("accommodation_charge", 0))),
                miscellaneous_charge=Decimal(str(billing_data.get("miscellaneous_charge", 0))),
                subtotal=subtotal,
                discount_amount=discount,
                discount_reason=billing_data.get("discount_reason"),
                tax_amount=tax_amount,
                tax_percentage=tax_percentage,
                total_amount=total_amount,
                balance_amount=total_amount,
                payment_status=PaymentStatus.PENDING,
                notes=billing_data.get("notes")
            )
            
            self.db.add(billing)
            self.db.commit()
            self.db.refresh(billing)
            
            # Add billing items
            for item in billing_data.get("items", []):
                billing_item = BillingItem(
                    billing_id=billing.id,
                    service_id=item.get("service_id"),
                    item_description=item["description"],
                    item_code=item.get("code"),
                    quantity=Decimal(str(item.get("quantity", 1))),
                    unit_price=Decimal(str(item["unit_price"])),
                    total_price=Decimal(str(item.get("total_price", 0))),
                    panel_rate=Decimal(str(item.get("panel_rate", 0))) if item.get("panel_rate") else None,
                    discount_amount=Decimal(str(item.get("discount", 0))),
                    tax_amount=Decimal(str(item.get("tax", 0))),
                    bill_date=date.today()
                )
                self.db.add(billing_item)
            
            self.db.commit()
            
            return {
                "success": True,
                "message": "Billing created successfully",
                "billing_id": billing.id,
                "invoice_number": billing.invoice_number,
                "total_amount": float(billing.total_amount)
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def get_billing(self, hospital_id: int, billing_id: int) -> Optional[Dict[str, Any]]:
        """Get billing by ID.
        
        Args:
            hospital_id: Hospital ID
            billing_id: Billing ID
            
        Returns:
            Billing data or None
        """
        try:
            billing = self.db.query(Billing).filter(
                Billing.id == billing_id,
                Billing.hospital_id == hospital_id
            ).first()
            
            if billing:
                items = self.db.query(BillingItem).filter(BillingItem.billing_id == billing_id).all()
                
                return {
                    "id": billing.id,
                    "invoice_number": billing.invoice_number,
                    "invoice_date": billing.invoice_date,
                    "patient_id": billing.patient_id,
                    "subtotal": float(billing.subtotal),
                    "discount_amount": float(billing.discount_amount),
                    "tax_amount": float(billing.tax_amount),
                    "total_amount": float(billing.total_amount),
                    "amount_paid": float(billing.amount_paid),
                    "balance_amount": float(billing.balance_amount),
                    "payment_status": billing.payment_status.value,
                    "billing_type": billing.billing_type.value,
                    "items": [
                        {
                            "description": item.item_description,
                            "quantity": float(item.quantity),
                            "unit_price": float(item.unit_price),
                            "total_price": float(item.total_price)
                        }
                        for item in items
                    ]
                }
            return None
        except Exception:
            return None

    def record_payment(self, hospital_id: int, billing_id: int, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record payment against billing.
        
        Args:
            hospital_id: Hospital ID
            billing_id: Billing ID
            payment_data: Payment data
            
        Returns:
            Payment result
        """
        try:
            billing = self.db.query(Billing).filter(
                Billing.id == billing_id,
                Billing.hospital_id == hospital_id
            ).first()
            
            if not billing:
                return {"success": False, "error": "Billing not found"}
            
            amount_paid = Decimal(str(payment_data["amount_paid"]))
            
            # Create payment record
            payment = Payment(
                billing_id=billing_id,
                payment_date=date.today(),
                payment_time=datetime.now().strftime("%H:%M"),
                payment_mode=PaymentMode[payment_data["payment_mode"].upper()],
                amount_paid=amount_paid,
                receipt_number=f"RCP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                reference_number=payment_data.get("reference_number"),
                remarks=payment_data.get("remarks"),
                received_by=payment_data.get("received_by"),
                bank_name=payment_data.get("bank_name"),
                cheque_number=payment_data.get("cheque_number"),
                cheque_date=payment_data.get("cheque_date"),
                transaction_id=payment_data.get("transaction_id")
            )
            
            self.db.add(payment)
            
            # Update billing
            billing.amount_paid += amount_paid
            billing.balance_amount = billing.total_amount - billing.amount_paid
            
            if billing.balance_amount <= 0:
                billing.payment_status = PaymentStatus.PAID
            elif billing.amount_paid > 0:
                billing.payment_status = PaymentStatus.PARTIAL
            
            self.db.commit()
            
            return {
                "success": True,
                "message": "Payment recorded successfully",
                "receipt_number": payment.receipt_number,
                "remaining_balance": float(billing.balance_amount)
            }
        except Exception as e:
            self.db.rollback()
            return {"success": False, "error": str(e)}

    def list_billings(self, hospital_id: int, status: str = None, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        """List billings.
        
        Args:
            hospital_id: Hospital ID
            status: Filter by payment status
            skip: Skip records
            limit: Limit records
            
        Returns:
            List of billings
        """
        try:
            query = self.db.query(Billing).filter(Billing.hospital_id == hospital_id)
            
            if status:
                query = query.filter(Billing.payment_status == PaymentStatus[status.upper()])
            
            total = query.count()
            billings = query.offset(skip).limit(limit).all()
            
            return {
                "success": True,
                "total": total,
                "billings": [
                    {
                        "id": b.id,
                        "invoice_number": b.invoice_number,
                        "invoice_date": b.invoice_date,
                        "patient_id": b.patient_id,
                        "total_amount": float(b.total_amount),
                        "balance_amount": float(b.balance_amount),
                        "payment_status": b.payment_status.value
                    }
                    for b in billings
                ]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
