# Use this file to easily define all of your cron jobs.
#
# It's helpful, but not entirely necessary to understand cron before proceeding.
# http://en.wikipedia.org/wiki/Cron

app_path = "/home/ubuntu/crispy-succotash"
log_path = "#{app_path}/log"
set :output, {error: "#{log_path}/cron_error_log.log", standard: "#{log_path}/cron_log.log"}

job_type :python_script, "source #{app_path}/VIRTUAL/bin/activate && cd #{app_path} && python app.py"

every "day", at: %w(8:00am 4:00pm) do
  command "source #{app_path}/VIRTUAL/bin/activate && cd #{app_path} && python app.py"
end

