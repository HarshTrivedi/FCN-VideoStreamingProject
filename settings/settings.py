# # A] Main experiment (1) with playback buffer finishing after competing flow introduction
experiment_duration       = 600
competing_flow_start_at   = 200
competing_flow_duration   = 300
playback_buffer_limit     = 200
playback_rate_selection   = True
smoothing                 = 10
segment_seconds           = 4
optimistic                = False
radical_client            = False

# # B] Main experiment (1) with playback buffer finishing after competing flow introduction
# experiment_duration       = 700
# competing_flow_start_at   = 100
# competing_flow_duration   = 500
# playback_buffer_limit     = 300
# playback_rate_selection   = True
# smoothing                 = 10
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# C] It's A without Rate Selection
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = False
# fixed_bitrate             = 1750*1024 # bits/s
# smoothing                 = 10
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# D] It's B without Rate Selection
# experiment_duration       = 700
# competing_flow_start_at   = 100
# competing_flow_duration   = 500
# playback_buffer_limit     = 250
# playback_rate_selection   = False
# fixed_bitrate             = 1750*1024 # bits/s
# smoothing                 = 10
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# E] No competing flow
# experiment_duration       = 400
# competing_flow_start_at   = 400
# competing_flow_duration   = 0
# playback_buffer_limit     = 300
# playback_rate_selection   = True
# smoothing                 = 10
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# F] A with twice the smoothing
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 20
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# # G] A with half the smoothing
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 5
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# # H] A with half the smoothing
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 1
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# # I] A with half the smoothing
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 100
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# J] A with half the smoothing
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 50
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# K] A with 1 fourth segment size
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 10
# segment_seconds           = 1
# optimistic                = False
# radical_client            = False

# # L] A with 2ce segment size
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 10
# segment_seconds           = 8
# optimistic                = False
# radical_client            = False

# # M] A with optimism
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 10
# segment_seconds           = 4
# optimistic                = True
# radical_client            = False

# # N] A with extremely high rate selection
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = False
# fixed_bitrate             = 3400*1024 # bits/s
# smoothing                 = 10
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False

# # O] A with extremely low rate selection
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = False
# fixed_bitrate             = 235*1024 # bits/s
# smoothing                 = 10
# segment_seconds           = 4
# optimistic                = False
# radical_client            = False


# # P] A with radical throw change!
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 10
# segment_seconds           = 4
# optimistic                = False
# radical_client            = True


# # Q] A with radical throw change + Optimism!
# experiment_duration       = 600
# competing_flow_start_at   = 200
# competing_flow_duration   = 300
# playback_buffer_limit     = 200
# playback_rate_selection   = True
# smoothing                 = 10
# segment_seconds           = 4
# optimistic                = True
# radical_client            = True

