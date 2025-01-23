import rules

@rules.predicate
def can_add_product(user):
    if not hasattr(user, "is_active"):
        return False  # anonymous user or swapped user model, doesn't support is_active field
    return (
        user.is_active
        & rules.is_authenticated(user)
        & (
            rules.is_superuser(user)
            
        )
    )


@rules.predicate
def can_view_product(user):
    if not hasattr(user, "is_active"):
        return False  # anonymous user or swapped user model, doesn't support is_active field
    return (
        user.is_active
        & rules.is_authenticated(user)
    )


@rules.predicate
def can_update_product(user):
    if not hasattr(user, "is_active"):
        return False  # anonymous user or swapped user model, doesn't support is_active field
    return (
        user.is_active
        & rules.is_authenticated(user)
        & (
            rules.is_superuser(user)
        )
    )


@rules.predicate
def can_delete_product(user):
    if not hasattr(user, "is_active"):
        return False  # anonymous user or swapped user model, doesn't support is_active field
    return (
        user.is_active
        & rules.is_authenticated(user)
        & (
            rules.is_superuser(user)
        )
    )