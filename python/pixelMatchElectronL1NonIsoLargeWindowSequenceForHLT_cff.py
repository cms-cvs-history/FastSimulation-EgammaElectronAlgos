import FWCore.ParameterSet.Config as cms

#
# create a sequence with all required modules and sources needed to make
# pixel based electrons
#
# NB: it assumes that ECAL clusters (hybrid) are in the event
#
#
# modules to make seeds, tracks and electrons

# Cluster-seeded pixel pairs
import FastSimulation.EgammaElectronAlgos.fastElectronSeeds_cfi
from FastSimulation.Configuration.blockHLT_8E29_cff import *

hltL1NonIsoLargeWindowElectronPixelSeeds = FastSimulation.EgammaElectronAlgos.fastElectronSeeds_cfi.fastElectronSeeds.clone()
hltL1NonIsoLargeWindowElectronPixelSeeds.SeedConfiguration = cms.PSet(
    block_hltL1NonIsoLargeWindowElectronPixelSeeds
)
hltL1NonIsoLargeWindowElectronPixelSeeds.barrelSuperClusters = 'hltCorrectedHybridSuperClustersL1NonIsolated'
hltL1NonIsoLargeWindowElectronPixelSeeds.endcapSuperClusters = 'hltCorrectedMulti5x5EndcapSuperClustersWithPreshowerL1NonIsolated'

# Track candidate
import FastSimulation.Tracking.TrackCandidateProducer_cfi

hltCkfL1NonIsoLargeWindowTrackCandidates = FastSimulation.Tracking.TrackCandidateProducer_cfi.trackCandidateProducer.clone()
hltCkfL1NonIsoLargeWindowTrackCandidates.SeedProducer = cms.InputTag("hltL1NonIsoLargeWindowElectronPixelSeeds")
hltCkfL1NonIsoLargeWindowTrackCandidates.TrackProducers = cms.VInputTag(cms.InputTag("hltCtfL1NonIsoWithMaterialTracks"))
hltCkfL1NonIsoLargeWindowTrackCandidates.MaxNumberOfCrossedLayers = 999
hltCkfL1NonIsoLargeWindowTrackCandidates.SeedCleaning = True
hltCkfL1NonIsoLargeWindowTrackCandidates.SplitHits = False


# CTF track fit with material
import RecoTracker.TrackProducer.CTFFinalFitWithMaterial_cfi

ctfL1NonIsoLargeWindowTracks = RecoTracker.TrackProducer.CTFFinalFitWithMaterial_cfi.ctfWithMaterialTracks.clone()
ctfL1NonIsoLargeWindowTracks.src = 'hltCkfL1NonIsoLargeWindowTrackCandidates'
ctfL1NonIsoLargeWindowTracks.TTRHBuilder = 'WithoutRefit'
ctfL1NonIsoLargeWindowTracks.Fitter = 'KFFittingSmootherForElectrons'
ctfL1NonIsoLargeWindowTracks.Propagator = 'PropagatorWithMaterial'

# Track merger
hltCtfL1NonIsoLargeWindowWithMaterialTracks = cms.EDFilter("FastTrackMerger",
    SaveTracksOnly = cms.untracked.bool(True),
    TrackProducers = cms.VInputTag(cms.InputTag("ctfL1NonIsoLargeWindowTracks"),
                                   cms.InputTag("hltCtfL1NonIsoWithMaterialTracks"))
)

# Sequence
HLTPixelMatchLargeWindowElectronL1NonIsoTrackingSequence = cms.Sequence(hltCkfL1NonIsoLargeWindowTrackCandidates+
                                                                        ctfL1NonIsoLargeWindowTracks+
                                                                        hltCtfL1NonIsoLargeWindowWithMaterialTracks+
                                                                        cms.SequencePlaceholder("hltPixelMatchLargeWindowElectronsL1NonIso"))

