#! /usr/bin/env python

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

files = ["tlbsm_53x_v3_mc.root"]
printGen = True
events = Events (files)
handle1  = Handle ("std::vector<pat::Jet>")
handle1a = Handle ("std::vector<pat::Jet>")
handle1b = Handle ("std::vector<pat::Jet>")
handle2  = Handle ("std::vector<pat::Jet>")
handle3  = Handle ("std::vector<pat::Jet>")
handle4  = Handle ("std::vector<pat::Muon>")
handle5  = Handle ("std::vector<pat::Electron>")

# for now, label is just a tuple of strings that is initialized just
# like and edm::InputTag
label1 = ("goodPatJetsCA8PrunedPF")
label1a= ("goodPatJetsCA8PrunedPFPacked")
label1b= ("selectedPatJetsCA8PrunedSubjetsPF")
label2 = ("goodPatJetsCATopTagPF")
label3 = ("goodPatJetsPFlow")
label4 = ("selectedPatMuonsPFlow")
label5 = ("selectedPatElectronsPFlow")

f = ROOT.TFile("ttbsm_unittest_fwlite.root", "RECREATE")
f.cd()


# loop over events
i = 0
nproblems = 0
for event in events:
    i = i + 1
    print  '--------- Processing Event ' + str(i)


    print '---- ' + label1
    # use getByLabel, just like in cmsRun
    event.getByLabel (label1, handle1)
    # get the product
    jets1 = handle1.product()

    ijet = 0
    for jet in jets1 :
        print 'Jet {0:4.0f}, pt = {1:6.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}, ptda0 = {6:6.2f}, ptda1 = {7:6.2f}'.format(
            ijet, jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.numberOfDaughters(), jet.daughter(0).pt(), jet.daughter(1).pt()
            )
        ijet += 1



    print '---- ' + label1a
    # use getByLabel, just like in cmsRun
    event.getByLabel (label1a, handle1a)
    # get the product
    jets1a = handle1a.product()

    dpt = 0.0
    for ijet in range(0,len(jets1a)) :
        jet = jets1a[ijet]
        print 'Jet {0:4.0f}, pt = {1:6.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}, ptda0 = {6:6.2f}, ptda1 = {7:6.2f}, bdiscda0 = {8:6.2f}, bdiscda1 = {9:6.2f}'.format(
            ijet, jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.numberOfDaughters(),
            jet.daughter(0).correctedP4(0).pt(), jet.daughter(1).correctedP4(0).pt(),
            jet.daughter(0).bDiscriminator('combinedSecondaryVertexBJetTags'), jet.daughter(1).bDiscriminator('combinedSecondaryVertexBJetTags'),
            )
        dpt = jets1[ijet].daughter(0).pt() - jets1a[ijet].daughter(0).correctedP4(0).pt()
        if abs(dpt) > 0.01 :
            nproblems += 1
            print "-------"
            print "-------"
            print "    BIG PROBLEM!!!! "
            print " pt_unpacked = " + str(jets1[ijet].daughter(0).pt()) + ", pt_packed = " +str(jets1a[ijet].daughter(0).correctedP4(0).pt()) + ", dpt = " +str(dpt)
            print "-------"
            print "-------"

    ## print '---- ' + label1b
    ## # use getByLabel, just like in cmsRun
    ## event.getByLabel (label1b, handle1b)
    ## # get the product
    ## jets1b = handle1b.product()

    ## dpt = 0.0
    ## for ijet in range(0,len(jets1b)) :
    ##     jet = jets1b[ijet]
    ##     print 'Jet {0:4.0f}, pt = {1:6.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, bdisc = {5:6.2f}'.format(
    ##         ijet, jet.pt(), jet.eta(), jet.phi(), jet.mass(), 
    ##         jet.bDiscriminator('combinedSecondaryVertexBJetTags')
    ##         )


    print '---- ' + label2
    # use getByLabel, just like in cmsRun
    event.getByLabel (label2, handle2)
    # get the product
    jets2 = handle2.product()

    ijet = 0
    for jet in jets2 :
        print 'Jet {0:4.0f}, pt = {1:6.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}, topmass = {6:6.2f}, minmass = {7:6.2f}'.format(
            ijet, jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.numberOfDaughters(), jet.tagInfo('CATop').properties().topMass, jet.tagInfo('CATop').properties().minMass
            )
        ijet += 1

        
    print '---- ' + label3
    # use getByLabel, just like in cmsRun
    event.getByLabel (label3, handle3)
    # get the product
    jets3 = handle3.product()

    ijet = 0
    for jet in jets3 :
        print ("Jet {0:4.0f}, pt = {1:6.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, " +
               "nda = {5:3.0f}, vtxmass = {6:6.2f}, area = {7:6.2f}, L1 = {8:6.2f}, L2 = {9:6.2f}, L3 = {10:6.2f}, " +
               "currLevel = {11:s}").format(
            ijet, jet.pt(), jet.eta(), jet.phi(), jet.mass(), jet.numberOfDaughters(), jet.userFloat('secvtxMass'),
            jet.jetArea(), jet.jecFactor("L1FastJet"), jet.jecFactor("L2Relative"), jet.jecFactor("L3Absolute"), jet.currentJECLevel()
            ),
        if printGen :
            genPt = 0.
            if jet.genJetFwdRef().isNonnull() and jet.genJetFwdRef().isAvailable() :
                genPt = jet.genJetFwdRef().pt()
            else :
                genPt = -1.0
            print (", gen pt = {0:6.2f}").format( genPt )
        else :
            print ''
        ijet += 1


    ## print '---- ' + label4
    ## # use getByLabel, just like in cmsRun
    ## event.getByLabel (label4, handle4)
    ## # get the product
    ## muons1 = handle4.product()

    ## imuon = 0
    ## for muon in muons1 :
    ##     if not muon.isGlobalMuon() :
    ##         continue
    ##     print 'Muon {0:4.0f}, pt = {1:6.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}, chi2/dof = {6:6.2f}'.format(
    ##         imuon, muon.pt(), muon.eta(), muon.phi(), muon.mass(), muon.numberOfDaughters(), muon.normChi2()
    ##         )
    ##     imuon += 1

    ## print '---- ' + label5
    ## # use getByLabel, just like in cmsRun
    ## event.getByLabel (label5, handle5)
    ## # get the product
    ## electrons1 = handle5.product()

    ## ielectron = 0
    ## for electron in electrons1 :
    ##     print 'Electron {0:4.0f}, pt = {1:6.2f}, eta = {2:6.2f}, phi = {3:6.2f}, m = {4:6.2f}, nda = {5:3.0f}, eidTightMC = {6:6.2f}'.format(
    ##         ielectron, electron.pt(), electron.eta(), electron.phi(), electron.mass(), electron.numberOfDaughters(), electron.electronID('eidTightMC')
    ##         )
    ##     ielectron += 1 



print 'we had : ' + str(nproblems) + ' problems'
f.cd()

f.Close()
