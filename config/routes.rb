Courts::Application.routes do
  add [],              HomeResource
  add ['courts'],      CourtsResource
  add ['courts', :id], CourtResource
end
