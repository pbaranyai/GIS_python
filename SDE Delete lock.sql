Delete from sde.SDE_table_locks
where sde_id not in (select sde_id from sde.SDE_process_information)

Delete from sde.SDE_layer_locks
where sde_id not in (select sde_id from sde.SDE_process_information)

Delete from sde.SDE_object_locks
where sde_id not in (select sde_id from sde.SDE_process_information)

Delete from sde.SDE_state_locks
where sde_id not in (select sde_id from sde.SDE_process_information)