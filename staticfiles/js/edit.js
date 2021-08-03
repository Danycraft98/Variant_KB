function get_report(elem, gene_pk, var_pk) {
    const dx_id = elem.id.split('_')[1].slice(0, -4), dx_name = elem.value;

    if (!dx_name.length) return;
    $.get('/api/diseases/' + dx_name, function (data) {
        let gdr_text = $('#id_' + dx_id + 'report-2-content'),
            vdr_text = $('#id_' + dx_id + 'report-3-content'),
            dx_data = data.length > 0 ? data[0] : {gene: -1, variant: -1};

        gdr_text.text(dx_data.gene === gene_pk ? dx_data.gdr : '')
        $('#id_' + dx_id + 'report-0-content').text(gdr_text.text());

        vdr_text.text(dx_data.variant === var_pk ? dx_data.vdr : '');
        $('#id_' + dx_id + 'report-1-content').text(vdr_text.text());
    }).fail(function () {
        console.log('error');
    });
}


function setClinSig(elem) {
    const selected = elem.val() === 'Diag' ? 'Dx' : elem.val(),
        act_div = elem.parents('dl');

    act_div.find("[id*='clin_sig']").children().each(function () {
        let curr = $(this)
        if (curr.val().includes(selected)) {
            curr.removeAttr('hidden')
        } else {
            curr.attr('hidden', '')
        }
    })

}


function setHeader(elem) {
    let dx_id = elem.id.slice(0, -4),
        dx_label = $('#' + dx_id + 'label'),
        dx_tab = $('#' + dx_id + 'tab'),
        dx_review = $('input[id*="' + dx_id + 'reviewed"]:checked');

    if (dx_review.length > 1) dx_review = dx_review.last().text();
    else dx_review = 'Not Reviewed';
    dx_label.text(elem.value + ' / ' + dx_review)
    dx_tab.text(dx_tab.text().replace(/[ ]{2,}|[\n\r]+/g, '').slice(0, 12) + elem.value)
}


function add_disease(main_elem) {
    if (main_elem.val() === 'no') return;
    let branch = main_elem.val(),
        tab = main_elem.parents('#tab-content')
            .prev().find("[id*='" + branch + "'][id*='tab']:hidden").first();
    new bootstrap.Tab(document.querySelector('#' + tab.attr('id'))).show()
    tab.first().removeAttr('hidden').tab('show');
    $(tab.attr('href')).find("[id*='branch']").val(branch);
    main_elem.val('no');
}


function add_item(elem, is_func = false) {
    let par_elem = elem.parents("dl[class*='row'], fieldset[id*='-div']:not([id*='outer'])"), container = elem.parents("div[id$='-form']"),
        pat = /(?:id_)?(.+?(?:item|func|act)-)(\d+)-div/g, match = pat.exec(par_elem.last().attr('id'));
    if (match) {
        let is_path = match[1].includes('item'),
            extra = is_path ? ' dl:last' : ':hidden',
            index = Math.floor(parseInt(match[2]) / 3), hidden;

        for (let i = index * 3; i < (index + 1) * 3; i++) {
            i = is_func ? i * 3 : i;
            hidden = container.find(`[id*='${match[1] + i.toString()}-div']${extra}`);
            if (hidden.length && hidden.attr('hidden') || hidden.hasClass('hidden')) {
                console.log('tete')
                hidden.removeClass('hidden').removeAttr('hidden').addClass('show');
                break;
            }
        }
    }
}


function delete_item(elem, is_func = false) {
    let parent = is_func ? elem.parent().parent().parent() : elem.parent().parent();
    parent.find(":input:not([id*='source_type'],[id*='item'],:hidden)").val('');
    parent.attr('hidden', '');
}


/* PVS = 10; PS = 7; PM = 2; PP = 1 || BA = 16; BS = 8; BP = 1
 * P:  12-14, 17; LP: 6, 9, 11, 12  ||  B:  16; LB: 2, 9 */
function calculate_score(main_elem) {
    let forScore = 0, againstScore = 0,
        prefix = main_elem.attr('id').slice(0, main_elem.attr('id').indexOf("-path_item"));

    $.each($(`:checkbox[id*='${prefix}']:checked`), function (_, curr) {
        let key = $(curr), score = parseInt(key.val()),
            score_label = key.parent().text().replace(/[ \n\r]/g, '')[0];

        if (score_label === 'P') forScore += score;
        else againstScore += score;
    });

    $.each($(`:checkbox[id*='${prefix}']:not(:checked)`), function (_, curr) {
        $.each($(curr).parent().attr('data-bs-target').split(','), function (_, div_id) {
            $(div_id).find('input:not(:hidden)').val('');
        });

    });

    if (forScore > 11) forScore = 'Pathogenic';
    else if (forScore > 5) forScore = 'Likely Pathogenic';
    else forScore = 'Uncertain';

    if (againstScore > 15) againstScore = 'Benign';
    else if (againstScore > 1) againstScore = 'Likely Benign';
    else againstScore = 'Uncertain';

    $(`#id_${prefix}-score-for_score`).val(forScore);
    $(`#id_${prefix}-score-against_score`).val(againstScore);

    const acmgClass = $(`#id_${prefix}-score-content`);
    if (forScore.includes('Pathogenic')) {
        if (againstScore === 'Uncertain') acmgClass.val(forScore);
        else if (againstScore.includes('Benign')) acmgClass.val('VUS');
    } else if (againstScore.includes('Benign')) acmgClass.val(againstScore);
    else acmgClass.val('Uncertain');
}


function tierChange(elem, options) {
    let pane_div = elem.parents("[id^='so-dx'][id*='-form']"),
        selected = options.includes(elem.val()),
        result = pane_div.find("[id*='others']");

    result.attr('disabled', selected).val('Tier IV');
    pane_div.children("[id*='act']").find('dd,dt').not('.other')
        .attr('hidden', selected);
    if (selected) pane_div.children("[id*='act']").find(":input:not([id*='type'],[type='hidden'])").val('');
}


function add_options(file, div_id) {
    $.get(file, function (data) {
        $.map(data, function (val, key) {
            let grp = $(`<optgroup label='${key}'></optgroup>`)
            $.each(val, function (_, item) {
                grp.append($(`<option value='${item}'>${item}</option>`));
            })
            $(div_id).append(grp);
        })
    });
}

function enable_second(element) {
    if ($(element).text().includes('Reviewed'))
        $($(element).parents('dd').children()[2]).removeAttr('disabled')
}

function update_notes(text) {
    $.each($("[id*='gene_curation_notes']"), function (i, sub_elem) {
        $(sub_elem).val(text.value);
    });
}

function submitMsg() {
    $('hidden').removeAttr('hidden')
    const checkboxes = document.querySelectorAll('input[name="review"]:checked');
    return confirm(checkboxes.length > 0 ? 'Do you want to update?' : 'Do you want to save?');
}

function modelMatcher(params, data) {
    data.parentText = data.parentText || "";

    // Always return the object if there is nothing to compare
    if ($.trim(params.term) === '') {
        return data;
    }

    // Do a recursive check for options with children
    if (data.children && data.children.length > 0) {
        // Clone the data object if there are children
        // This is required as we modify the object to remove any non-matches
        var match = $.extend(true, {}, data);

        // Check each child of the option
        for (var c = data.children.length - 1; c >= 0; c--) {
            var child = data.children[c];
            child.parentText += data.parentText + " " + data.text;

            var matches = modelMatcher(params, child);

            // If there wasn't a match, remove the object in the array
            if (matches == null) {
                match.children.splice(c, 1);
            }
        }

        // If any children matched, return the new object
        if (match.children.length > 0) {
            return match;
        }

        // If there were no matching children, check just the plain object
        return modelMatcher(params, match);
    }

    // If the typed-in term matches the text of this term, or the text from any
    // parent term, then it's a match.
    var original = (data.parentText + ' ' + data.text).toUpperCase();
    var term = params.term.toUpperCase();


    // Check if the text contains the term
    if (original.indexOf(term) > -1) {
        return data;
    }

    // If it doesn't contain the term, don't return anything
    return null;
}