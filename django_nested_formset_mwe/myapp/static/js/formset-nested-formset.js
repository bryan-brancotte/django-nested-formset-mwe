function add_form_to_nested_formset(source, prefix){
    let input_total=$(source).closest(".formset-container").find("[name='"+prefix+"-TOTAL_FORMS']");
    let empty_form_as_str = $(source).closest(".formset-container").find(".empty_form").prop('innerHTML');
    empty_form_as_str = empty_form_as_str.replace(
        new RegExp(prefix+"-__prefix__","g"),
        prefix+"-"+input_total.val()
    );
    empty_form=$(empty_form_as_str );
    empty_form.find(".formset-nested-item").first().remove();
    empty_form.insertBefore($(source).parent());
    input_total.val(parseInt(input_total.val())+1);
    return empty_form;

}

function add_nested_form_to_nested_formset(source, prefix, parent_prefix){
    let empty_form_as_str = $(source)
        .closest(".formset-container")
        .find(".empty_form")
        .find(".formset-nested-item")[0]
        .outerHTML;

    current_item_name = $(source).closest(".formset-item").children("input")[0].name;
    current_item_name = current_item_name.substring(parent_prefix.length+1,current_item_name.indexOf('-',parent_prefix.length+1));
    empty_form_as_str = empty_form_as_str.replace(
        new RegExp(parent_prefix+"-__prefix__","g"),
        parent_prefix+"-"+current_item_name

    );

    let input_total=$(source).closest(".formset-item").find("[name='"+prefix+"-TOTAL_FORMS']");
    empty_form_as_str = empty_form_as_str.replace(
        new RegExp(prefix+"-__prefix__","g"),
        prefix+"-"+input_total.val()
    );

    let empty_form=$(empty_form_as_str);
    empty_form.insertBefore($(source).parent());
    input_total.val(parseInt(input_total.val())+1);
    return empty_form;
}

function delete_button_clicked(source) {
    let item = $(source).closest(".form-group");
    $(item).addClass("formset-item-delete-host");
    item = $(item).closest(".formset-nested-item");
    if (item.length==0){
        item = $(source).closest(".formset-item");
    }
    if ($(source).prop("checked")){
        $(item).addClass("delete-checked");
    }else{
        $(item).removeClass("delete-checked");
    }
}