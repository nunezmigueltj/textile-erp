from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from .models import PullRequest, PullRequestLine
from .forms import PullRequestForm, PullRequestLineForm, PullRequestLineInlineFormSet
from django.forms.models import inlineformset_factory

# Create your views here.
def pullrequest_list(request): 
    q = request.GET.get('q')
    DEFAULT_ROWS_PER_PAGE = 25 # default to 25
    rows_per_page = request.GET.get('rowsPerPage', DEFAULT_ROWS_PER_PAGE)

    try:
        rows_per_page = int(rows_per_page)
    except ValueError:
        rows_per_page = DEFAULT_ROWS_PER_PAGE

    fabric_pulls = PullRequest.objects.select_related('purchase_order').order_by('-id')

    if q:
        q=q.strip()
        fabric_pulls = fabric_pulls.filter(
                Q(purchase_order__po_number__icontains=q) |
                Q(created_at__icontains=q) |
                Q(status__icontains=q) |
                Q(purchase_order__fabrics__fabric__fabric__item_code__icontains=q) |
                Q(purchase_order__fabrics__fabric__fabric__vendor_code__icontains=q) |
                Q(purchase_order__fabrics__fabric__fabric__cuttable__icontains=q) |
                Q(purchase_order__fabrics__fabric__color__name__icontains=q) |
                Q(purchase_order__fabrics__fabric__color__code__icontains=q) |
                Q(lines__requested_yards__icontains=q) | 
                Q(notes__icontains=q)
            ).distinct().order_by('-id')

        
    paginator = Paginator(fabric_pulls, rows_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pullrequest/pullrequest_list.html', {'page_obj': page_obj, 
                                                 'rows_per_page': rows_per_page})

def issue_pull_request(request):
    LineFormSet = inlineformset_factory(
        PullRequest,
        PullRequestLine,
        form=PullRequestLineForm,
        fields=['inventory_roll', 'requested_yards', 'notes'],
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        pullrequest_form = PullRequestForm(request.POST)

        if pullrequest_form.is_valid():
            with transaction.atomic():
                receipt = pullrequest_form.save(commit=False)
                receipt.created_by = request.user if request.user.is_authenticated else None
                receipt.save()

                # define prefix for the formset to avoid conflicts with other forms on the page
                line_formset = LineFormSet(request.POST, instance=receipt, prefix='lines')

                if line_formset.is_valid():
                    lines = line_formset.save(commit=False)
                    for line in lines:
                        line.save()
                    for line in line_formset.deleted_objects:
                        line.delete()
                else:
                    # if not valid, rollback exception will be raised and transaction will be rolled back
                    raise transaction.TransactionManagementError("Formset invalid")
            return redirect('pullrequest:pullrequest_list')
    else:
        pullrequest_form = PullRequestForm()
        line_formset = LineFormSet(prefix='lines')

    return render(request, 'pullrequest/issue_pull_request.html', {
        'pullrequest_form': pullrequest_form,
        'line_formset': line_formset,
    })